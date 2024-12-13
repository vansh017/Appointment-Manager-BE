import json
from typing import List

from fastapi import Request

import crud
import dao
from core import TSServerError, TSResponse, api_log
from dao import get_customer_queue
from dao.shop import create_shop
from models import UserModel
from schemas import CatalogSchema
from utilities.methods import log_method_resp_time


@log_method_resp_time(msg="getting response")
def _add_customer_queue(*args,**kwargs):
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
        shop_data = kwargs['shop_data']
        shop_id = shop_data.get("shop_id")
        if user:
            user = user[0]
        else:
            raise TSServerError(
                error=TSServerError.USER_NOT_FOUND,
                status_code=200)

        customer = dao.add_customer_to_queue(db=db, shop_id=shop_id,user=user)
        db.commit()

        return TSResponse(customer)

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e


@log_method_resp_time(msg="getting shops ")
def _get_customer_queue(*args,**kwargs):
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
        shop = get_customer_queue(db=db, filters=filters, sort_fields=sort_fields, paginate=paginate,shop_id=shop_id)
        db.commit()

        return TSResponse(shop)

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e