from sqlalchemy import delete
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

BearerToken = CRUDBearerToken(BearerTokenModel)
