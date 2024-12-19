

from fastapi import APIRouter, Request, Depends, Body
from fastapi.params import Query
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from api.api_v1.endpoints.websocket import connection_manager
from constants import OpenApiTags
from api.api_v1.deps import get_db
from core import api_log, create_response, create_error_response, TSServerError
from services.customer_service import _add_customer_queue, _get_customer_queue

customer = APIRouter(
    prefix="/customer",
    tags=[OpenApiTags.CUSTOMER],
    dependencies=[Depends(HTTPBearer())]

)


@customer.post("", name="Join Customer Queue",
           description="Customer queue")
async def create_customer_row(*, request: Request,
                        user_id: int = Query(default=None),
                        shop_data = Body(),
                        db: Session = Depends(get_db),
                        ):
    """
    Login route for user ... sends otp on user's email
    the user will be marked as in active when he/she enters wrong password multiple times
    :param shop_data:
    :param user_id:
    :param request:
    :param db:
    :return:
    """
    try:
        response = _add_customer_queue(db=db, request=request,shop_data=shop_data,user_id=user_id)

        updated_queue = await _get_customer_queue(db=db, request=request,shop_id=shop_data.get("shop_id"),user_id=user_id,
                                       filters=None,sort_fields=None,paginate=None)

        await connection_manager.broadcast_to_shop(updated_queue.data,shop_id=int(shop_data.get("shop_id")))

        return create_response(response.data)

    except TSServerError as err:
        return create_error_response(status_code=err.status_code, err_dict=err.__dict__())

    except Exception as e:
        api_log.error(f"exception in authenticating user: {e}", exc_info=True)
        return create_error_response(TSServerError.INTERNAL_SV_ERROR)


@customer.get("", name="Join Customer Queue",
           description="Customer queue")
async def get_customers(*, request: Request,
                  user_id: int = Query(default=None),
                  shop_id: int = Query(default=None),
                  db: Session = Depends(get_db),
                  filters=Query(default=None),
                  sort_fields=Query(default=None),
                  paginate=Query(default=None),
                  ):
    """
    Login route for user ... sends otp on user's email
    the user will be marked as in active when he/she enters wrong password multiple times
    :param shop_id:
    :param user_id:
    :param request:
    :param db:
    :param filters:
    :param sort_fields:
    :param paginate:
    :return:
    """
    try:
        response = await _get_customer_queue(db=db, request=request,shop_id=shop_id,user_id=user_id,
                                       filters=filters,sort_fields=sort_fields,paginate=paginate)

        return create_response(response.data)

    except TSServerError as err:
        return create_error_response(status_code=err.status_code, err_dict=err.__dict__())

    except Exception as e:
        api_log.error(f"exception in authenticating user: {e}", exc_info=True)
        return create_error_response(TSServerError.INTERNAL_SV_ERROR)