import json

from fastapi import Request

import crud
from core import TSServerError, TSResponse, api_log
from dao.shop import create_shop, get_shops, get_shop_menu
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


@log_method_resp_time(msg="getting shops ")
def _get_shops(*args,**kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """
    try:
        db = kwargs['db']
        request : Request = kwargs['request']
        user_id = kwargs['user_id']
        role = kwargs['role']
        user: [UserModel] = crud.User.get(db=db,id=user_id)
        filters = kwargs['filters']
        sort_fields = kwargs['sort_fields']
        paginate = kwargs['paginate']

        if not user:
            raise TSServerError(
            status_code=200,
            error=TSServerError.USER_NOT_FOUND,
        )
        user = user[0]

        json_filter_err = TSServerError(
            status_code=200,
            error=TSServerError.INTERNAL_SV_ERROR,
        )
        try:
            if filters:
                filters = json.loads(filters)

            if sort_fields:
                sort_fields = json.loads(sort_fields)

            if paginate:
                paginate = json.loads(paginate)

        except Exception as e:
            api_log.exception(f"json loads error: {e}")
            raise json_filter_err
        filters = {}
        if role =="shop_owner":
            filters['user_id'] = user.id
        shop = get_shops(db=db, filters=filters, sort_fields=sort_fields, paginate=paginate)
        db.commit()

        return TSResponse(shop)

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e

@log_method_resp_time(msg="getting shops ")
def _get_shop_menu(*args,**kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """
    try:
        db = kwargs['db']
        request : Request = kwargs['request']
        user_id = kwargs['user_id']
        shop_id = kwargs['shop_id']
        user: [UserModel] = crud.User.get(db=db,id=user_id)
        filters = kwargs['filters']
        sort_fields = kwargs['sort_fields']
        paginate = kwargs['paginate']

        if not user:
            raise TSServerError(
            status_code=200,
            error=TSServerError.USER_NOT_FOUND,
        )
        user = user[0]

        json_filter_err = TSServerError(
            status_code=200,
            error=TSServerError.INTERNAL_SV_ERROR,
        )
        try:
            if filters:
                filters = json.loads(filters)

            if sort_fields:
                sort_fields = json.loads(sort_fields)

            if paginate:
                paginate = json.loads(paginate)

        except Exception as e:
            api_log.exception(f"json loads error: {e}")
            raise json_filter_err
        filters = {}
        shop = get_shop_menu(db=db,shop_id=shop_id, filters=filters, sort_fields=sort_fields, paginate=paginate)
        db.commit()

        return TSResponse(shop)

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e