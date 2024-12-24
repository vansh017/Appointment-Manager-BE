from typing import List

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from core import TSServerError, api_log
from crud import CRUDBase
from models import  BearerTokenModel

from schemas import  BearerTokenSchema


class CRUDBearerToken(CRUDBase[BearerTokenModel, BearerTokenSchema, BearerTokenSchema]):
    @classmethod
    def delete_previous_tokens(cls, db: Session, user_id: int):
        """
        Deletes all previously assigned token for the user
        :param db:
        :param user_id:
        :return:
        """
        try:
            query = delete(BearerTokenModel) \
                .filter(BearerTokenModel.user_id == user_id)

            db.execute(query)

        except TSServerError as err:
            raise err
        except Exception as e:
            api_log.exception(f"exception: {e}")
            raise TSServerError()

    @classmethod
    def get_access_token_info(cls, access_token: str, db: Session) -> List[BearerTokenModel]:
        """
        Retrieves token info for a given access_token
        :param access_token:
        :param db:
        :return:
        """
        try:

            query = select(BearerTokenModel) \
                .filter(BearerTokenModel.access_token == access_token,
                        BearerTokenModel.is_revoked == False)

            token_list = db.execute(query).all()

            token_list = [token[0] for token in token_list]

            return token_list
        except Exception as e:
            api_log.error(f"error in retrieving token data: {e}")
            raise TSServerError()

    @classmethod
    def revoke_access_token(cls, access_token: str, db: Session):
        """
        Revokes access_token, raises DPAuth Error if failed
        :param access_token: access token assigned to client
        :param db:
        :return:
        Revokes Tokens by setting is_revoked = True for a given access_token
        """
        try:
            db.query(BearerTokenModel) \
                .filter(BearerTokenModel.access_token == access_token) \
                .delete()

            db.flush()
        except Exception as e:
            db.rollback()
            api_log.error(f"failed to revoke access token: {e}", exc_info=True)
            raise TSServerError()

BearerToken = CRUDBearerToken(BearerTokenModel)
