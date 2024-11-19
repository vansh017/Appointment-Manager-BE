import bcrypt
from sqlalchemy.orm import Session

import crud
from constants import MAX_FAILED_LOGIN_FOR_USER, MAX_OTP_REQUEST_PER_HR
from core import TSServerError, get_current_date_time, api_log
from dao.otp import total_otp_request, get_unlock_time, create_otp
from models import UserModel
from schemas.api_schemas import CreateUser
from utilities.methods import create_pwd_hash


def create_user_dao(db: Session,user_data: CreateUser):
    """

    :param db:
    :param user_data:
    :return:
    """
    try:

        user_info = crud.User.get_by_email(db=db,email=user_data.email)
        if user_info:
            raise TSServerError(
                status_code=200,
                error=TSServerError.USER_EXIST,
            )

        hashed_pwd = create_pwd_hash(user_data.password)
        user = UserModel(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password=hashed_pwd,
            gender=user_data.gender,
            username=user_data.email,
            email=user_data.email,
            is_active=True,
            is_deleted=False,
            created_on=get_current_date_time(),
            modified_on=get_current_date_time()
        )
        db.add(user)
        db.flush([user])
        return user

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e
    
    
def validate_user_login_and_create_otp(db: Session, user: UserModel, password):
    """
    Validates user login which will check for failed login attempts and will
    lock account for max unsuccessful login attempts

    This is main method for db interaction commit/rollback is handled in this method
        - other functions which interacts with DB will issue a session flush
            ... the changes are not persisted in DB on using flush

    :param password: user password from request body
    :param db:
    :param user:
    :return:
    """
    try:
        # checking if user was previously blocked or not
        if not user.is_active:
            if user.failed_login_count == 0 and user.invalid_otp_count == 0:
                api_log.info(f"password is not created for user: {user.username}")
                raise TSServerError(
                    error=TSServerError.INVALID_USER_CRED,
                    status_code=200
                )
            else:
                api_log.info(f"user is not active: {user.username}")
                raise TSServerError(
                    error=TSServerError.USER_ACC_INACTIVE,
                    status_code=200
                )

        # # counting failed login attempts for the user
        # # ... if failed login attempt exceeded the limit user has to reset its password using forgot password flow
        # if user.failed_login_count and user.failed_login_count >= MAX_FAILED_LOGIN_FOR_USER:
        #     api_log.info(f"user has exceeded max unsuccessful login attempts: {user.id}")
        #     raise TSServerError(
        #         error=TSServerError.FAILED_LOGIN_ATTEMPT_LIMIT_EXCEEDED,
        #         status_code=200
        #     )

        hashed_pwd = user.password
        if not validate_password(password=password, hashed_pwd=hashed_pwd):
            # validating user's password ... if password is invalid user's failed login count will be incremented
            # ... if failed login count reached max limit user's account will be marked as in active and
            # he/she has to reset password
            api_log.info(f"invalid password for user: {user.id}")
            failed_login_attempts = crud.User.add_invalid_login_count(db=db, user_id=user.id)
            if failed_login_attempts >= MAX_FAILED_LOGIN_FOR_USER:
                api_log.info(f"failed login limit exceeded for the user: {user.id}, "
                             f"marking user as inactive")

                crud.User.mark_user_in_active(db=db, user_id=user.id)

            db.commit()  # once password is validated and failed login attempts are added ... issuing a commit

            if MAX_FAILED_LOGIN_FOR_USER == failed_login_attempts:
                raise TSServerError(
                    error=TSServerError.FAILED_LOGIN_ATTEMPT_LIMIT_EXCEEDED,
                    status_code=200
                )

            raise TSServerError(
                error=TSServerError.INVALID_USER_CRED,
                status_code=200,
                additional_info={
                    "login_attempts_left": MAX_FAILED_LOGIN_FOR_USER - failed_login_attempts
                }
            )

        # checking total OTP request in one hr from user...
        # once login is successful for the user all otp are deleted for the user this
        # check makes sure that user is able to request limited number otp in one hour
        total_attempts = total_otp_request(db=db, user_id=user.id)
        if total_attempts >= MAX_OTP_REQUEST_PER_HR:
            api_log.info(f"otp request exceeded for user: {user.username}")
            # no need to commit here as no insertion is done is here
            unlock_time = get_unlock_time(db=db, user_id=user.id)
            unlock_time = int(unlock_time / 60)
            raise TSServerError(
                error=TSServerError.OTP_REQUEST_LIMIT_EXCEEDED,
                status_code=200,
                additional_info={"retry_after": unlock_time}
            )

        # on successful login resetting user's failed login count to 0
        crud.User.reset_failed_login(db=db, user_id=user.id)
        otp = create_otp(db=db, user_id=user.id)

        total_attempts = total_otp_request(db=db, user_id=user.id)

        db.commit()

        return otp, total_attempts

    except TSServerError as err:
        # no rollback here ... as in case failed login attempts custom error is raised
        raise err
    except Exception as e:
        db.rollback()  # rollback in case of code failure
        api_log.exception(f"exception in validate_user_login: {e}")
        raise TSServerError()


def validate_password(password, hashed_pwd):
    try:
        if not bcrypt.checkpw(password=password.encode(), hashed_password=hashed_pwd.encode()):
            return False

        return True
    except Exception as e:
        api_log.error(f"exception in checking password: {e}", exc_info=True)
        raise TSServerError()

