from fastapi import Request

import crud
from core import TSServerError, TSResponse
from dao.shop import create_shop
from models import UserModel
from utilities.methods import log_method_resp_time


@log_method_resp_time(msg="getting response")
def _create_shop(*args,**kwargs):
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
        shop_details = kwargs['shop_details']
        if user:
            user = user[0]
        else:
            raise TSServerError(
                error=TSServerError.USER_NOT_FOUND,
                status_code=200)

        shop = create_shop(db=db, shop_details=shop_details,user=user)
        db.commit()

        return TSResponse(shop)

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e