import datetime

from fastapi import APIRouter, Request, Depends, Body
from sqlalchemy.orm import Session

from constants import OpenApiTags
from api.api_v1.deps import get_db
from core import api_log

auth = APIRouter(
    prefix="/auth",
    tags=[OpenApiTags.AUTH]
)


# @auth.post("/signup", name="Sign Up ",
#            description="API Authenticates user and sends OTP for login")
# def api_authenticate_user(*, request: Request,
#                           user_data: CreateUser = Body(),
#                           db: Session = Depends(get_db)):
#     """
#     Login route for user ... sends otp on user's email
#     the user will be marked as in active when he/she enters wrong password multiple times
#     :param user:
#     :param request:
#     :param db:
#     :return:
#     """
#     try:
#         response = create_user(db,request,user_data)
#         return create_response({})
#
#     except Exception as e:
#         api_log.error(f"exception in authenticating user: {e}", exc_info=True)
#         return create_error_response({})
