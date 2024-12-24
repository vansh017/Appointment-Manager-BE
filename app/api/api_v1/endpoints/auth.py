import datetime

from fastapi import APIRouter, Request, Depends, Body
from sqlalchemy.orm import Session

from constants import OpenApiTags
from api.api_v1.deps import get_db
from core import api_log, create_response, create_error_response, TSServerError
from schemas.api_schemas import CreateUser, ValidateOTP
from services.auth_service import create_user, login_user, authenticate_user, revoke_token

auth = APIRouter(
    prefix="/auth",
    tags=[OpenApiTags.AUTH]
)


@auth.post("/signup", name="Sign Up ",
           description="API Authenticates user and sends OTP for login")
def api_authenticate_user(*, request: Request,
                          user_data: CreateUser = Body(),
                          db: Session = Depends(get_db)):
    """
    Login route for user ... sends otp on user's email
    the user will be marked as in active when he/she enters wrong password multiple times
    :param user_data:
    :param request:
    :param db:
    :return:
    """
    try:
        response = create_user(db=db,request=request,user_data=user_data)
        return create_response(response)

    except TSServerError as err:
        return create_error_response(status_code=err.status_code, err_dict=err.__dict__())

    except Exception as e:
        api_log.error(f"exception in authenticating user: {e}", exc_info=True)
        return create_error_response(TSServerError.INTERNAL_SV_ERROR)

@auth.post("/login", name="Login Functionality",
           description="API Authenticates user and sends OTP for login")
def api_authenticate_user(*, request: Request,
                          user: dict = Body(),
                          db: Session = Depends(get_db)):
    """
    Login route for user ... sends otp on user's email
    the user will be marked as in active when he/she enters wrong password multiple times
    :param user:
    :param request:
    :param db:
    :return:
    """
    try:
        response = login_user(db=db,request=request,user=user)
        return create_response(response)

    except TSServerError as err:
        return create_error_response(status_code=err.status_code, err_dict=err.__dict__())

    except Exception as e:
        api_log.error(f"exception in authenticating user: {e}", exc_info=True)
        return create_error_response(TSServerError.INTERNAL_SV_ERROR)


@auth.post("/otp", name="Validates OTP for the user",
           description="API Validates OTP for the user")
def api_authenticate_user(*, request: Request,
                          user: ValidateOTP = Body(
                              example={
                                  "otp": 123456,
                                  "username": "username"
                              }
                          ),
                          db: Session = Depends(get_db)):
    """
    Login route for user -- only implicit grant is supported here
    User has to reset its password on entering wrong otp for 5 times
    :param user:
    :param request:
    :param db:
    :return:
    """
    try:

        response = authenticate_user(request=request, db=db, user=user)

        return create_response(data=response.data)
    except TSServerError as err:
        return create_error_response(status_code=err.status_code, err_dict=err.__dict__())
    except Exception as e:
        api_log.error(f"exception in authenticating user: {e}", exc_info=True)
        return create_error_response(TSServerError.INTERNAL_SV_ERROR)


@auth.post("/revoke", name="Validates OTP for the user",
           description="API Validates OTP for the user")
def api_authenticate_user(*, request: Request,
                          access_token = Body(),
                          db: Session = Depends(get_db)):
    """
    Login route for user -- only implicit grant is supported here
    User has to reset its password on entering wrong otp for 5 times
    :param access_token:
    :param request:
    :param db:
    :return:
    """
    try:

        response = revoke_token(request=request, db=db, access_token=access_token)

        return create_response(data=response.data)
    except TSServerError as err:
        return create_error_response(status_code=err.status_code, err_dict=err.__dict__())
    except Exception as e:
        api_log.error(f"exception in authenticating user: {e}", exc_info=True)
        return create_error_response(TSServerError.INTERNAL_SV_ERROR)