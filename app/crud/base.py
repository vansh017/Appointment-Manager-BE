"""
Description: File contains Base Class for CRUD Operations.
    CRUD Functions of this class is only based on ID

    Functions in the CRUD layer returns list of all the records as
    list[dict] type

    In case if no record is found empty list will be returned

    In case of any exception DpAuthError will be raised

    Since we can't pass our db: Session object to OAuth layer
    a new session is created everytime when OAuth calls any CRUD
    function that requires DB interaction
"""

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from db.base_class import Base
from sqlalchemy.orm import Session
from sqlalchemy import exc, select
from typing import Generic, TypeVar, Type, List, Union
from core import TSServerError, api_log

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(self, db: Session) -> ModelType:
        """
        Returns all ids for Model
        :param db:
        :return:
        """
        try:
            query = select(self.model)
            records = db.execute(query).all()

            record_list = [record[0] for record in records]

            return record_list

        except Exception as e:
            api_log.exception(f"failed to retrieve id's for model: {e}")
            raise FOServerError()

    def get(self, id: int, db: Session) -> List[ModelType]:
        """
        :param id: unique int id given to all records
        :param db: DB Object
        :return: required record as dict
        """
        try:
            record_list = db.query(self.model) \
                .filter(self.model.id == id) \
                .all()
            return record_list
        except Exception as e:
            api_log.error(f"failed to fetch data from DB: {e}")
            raise FOServerError()

    def update(self, id: int, update_dict: dict, db: Session):
        """
        Returns updated object
        Updates records in DB of id, update_dict should be a model dict
        :param id:
        :param update_dict:
        :param db:
        :return:
        """
        try:

            record = db.query(self.model)\
                .filter(self.model.id == id)\
                .all()

            if not len(record):
                api_log.error(f"no record to update for {self.model}, id: {id}")
            record = record[0]

            for key, value in update_dict.items():
                if hasattr(record, key):
                    setattr(record, key, value)
                else:
                    api_log.debug(f"record: {dict(record)} has not attribute: {key};"
                                  f" Aborting transaction")
                    raise FOServerError()

            db.flush([record])
            return record

        except Exception as e:
            api_log.error(f"failed to update in records in DB: {e}")
            raise FOServerError()

    def create(self, db: Session, record: CreateSchemaType) -> ModelType:
        """
        Creates a record in table commit/rollback should be handled outside this function
        :param db:
        :param record:
        :return: adds record in table, raises error on failure
        """
        try:
            record_dict = jsonable_encoder(record)
            record = self.model(**record_dict)
            db.add(record)
            db.flush([record])
            return record
        except Exception as e:
            api_log.error(f"failed to create record in DB: {e}")
            raise FOServerError()

    def add_multiple_records(self,db: Session, objects: List[CreateSchemaType]):
        """

        :param db:
        :param objects:
        :return:
        """
        try:
            db_records = [self.model(**(jsonable_encoder(obj))) for obj in objects]  # Convert Pydantic to SQLAlchemy models
            db.add_all(db_records)  # Add all records at once
            db.flush(db_records)
        except Exception as e:
            api_log.error(f"failed to create records in DB: {e}")
            raise FOServerError()

    def get_by_filter(self, db: Session, value, attribute, search_type="exact_search"):
        """
        Return records based on filter.
        :param search_type:
        :param db:
        :param value:
        :param attribute:
        :return:
        """
        try:
            query = select(self.model).filter(attribute == value)
            if search_type == "like_search":
                query = query.filter(attribute.like(f"%{value}%"))
            if search_type == "exact_search":
                query = query.filter(attribute == value)
            if search_type == "in_search":
                query = query.filter(attribute == value)

            records = db.execute(query).all()

            record_list = [record[0] for record in records]

            return record_list

        except Exception as e:
            api_log.error(f"failed to create record in DB: {e}")
            raise FOServerError()



