from sqlalchemy.orm import Session
import jwt

import crud
from core import TSServerError, api_log
from utilities.methods import SECRET_KEY


def revoke_token_process(db:Session,token : str):
    """

    :param db:
    :param token:
    :return:
    """
    try:
        # payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # print(payload)
        header, payload, signature = token.split(".")

        token_list = crud.BearerToken.get_access_token_info(access_token=payload, db=db)

        if not len(token_list):
            api_log.info("invalid token received")
            # The purpose of revocation endpoint is to revoke a particular a token
            # and since we couldn't find the given token in storage means token is
            # invalid, hence not raising any error
            return
        token_info = token_list[0]
        crud.BearerToken.revoke_access_token(access_token=payload, db=db)

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e