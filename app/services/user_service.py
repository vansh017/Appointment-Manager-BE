from fastapi import Request

import crud
from core import TSServerError, TSResponse
from models import UserModel
from utilities.methods import log_method_resp_time


@log_method_resp_time(msg="getting response")
def get_user_data(*args,**kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """
    try:
        db = kwargs['db']
        request : Request = kwargs['request']
        user_id = kwargs['user_id']
        user: UserModel = crud.User.get(db=db,id=user_id)
        if user:
            user = user[0]
        else:
            raise TSServerError(
                error=TSServerError.USER_NOT_FOUND,
                status_code=200)
        user_dict = dict(user_id=user.id,
                         first_name = user.first_name,
                         last_name=user.last_name,
                         email=user.email,
                         gender=user.gender,
                         contact_number=user.contact_number
                         )
        response = TSResponse(user_dict)
        return response

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e