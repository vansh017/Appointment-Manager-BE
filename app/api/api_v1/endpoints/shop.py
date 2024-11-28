import datetime

from fastapi import APIRouter, Request, Depends, Body
from fastapi.params import Query
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from constants import OpenApiTags
from api.api_v1.deps import get_db
from core import api_log, create_response, create_error_response, TSServerError
from services.user_service import get_user_data

shop = APIRouter(
    prefix="/shop",
    tags=[OpenApiTags.SHOP],
    dependencies=[Depends(HTTPBearer())]

)


@shop.post("/create", name="Create shop",
           description="Creating shop")
def api_authenticate_user(*, request: Request,
                          user_id: int = Query(default=None),
                          db: Session = Depends(get_db)):
    """
    Login route for user ... sends otp on user's email
    the user will be marked as in active when he/she enters wrong password multiple times
    :param user_id:
    :param request:
    :param db:
    :return:
    """
    try:
        response = get_user_data(db=db,request=request,user_id=user_id)

        return create_response(response.data)

    except TSServerError as err:
        return create_error_response(status_code=err.status_code, err_dict=err.__dict__())

    except Exception as e:
        api_log.error(f"exception in authenticating user: {e}", exc_info=True)
        return create_error_response(TSServerError.INTERNAL_SV_ERROR)

