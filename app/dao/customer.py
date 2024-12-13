
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import Session

import crud
from models import UserModel, CustomerQueueModel
from schemas import ShopSchema, CatalogSchema, CustomerQueueSchema
from schemas.api_schemas import CreateShop
from core import TSServerError, api_log
from schemas.customer_queue import CustomerStatusEnum


def add_customer_to_queue(db: Session, shop_id : int, user : UserModel):
    """

    :param db:
    :param shop_id:
    :param user:
    :return:
    """

    try:
        customer_obj = CustomerQueueSchema(customer_id=user.id,
                            shop_id=shop_id,
                            status = CustomerStatusEnum.WAITING.value)
        customer = crud.CustomerQueue.create(db=db, record=customer_obj)
        return customer

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e


def get_customer_queue(db:Session, shop_id :int,  filters : dict = None, sort_fields: list = None, paginate: dict = None):
    """

    :param db:
    :param filters:
    :param sort_fields:
    :param paginate:
    :param shop_id:
    :return:
    """
    try:
        if not sort_fields:
            sort_fields = []

        if not filters:
            filters = {}
        query = (select(CustomerQueueModel.id,
                        CustomerQueueModel.status,
                        CustomerQueueModel.customer_id,
                        UserModel.email,
                        func.concat(UserModel.first_name," ", UserModel.last_name).label("customer_name"),)
                 .join(UserModel, and_(CustomerQueueModel.customer_id == UserModel.id))
                 .filter(CustomerQueueModel.shop_id == shop_id)
                 )

        filter_clause = list()
        args_mapper = {
            "user_id": UserModel.id
        }
        exact_search = ['user_id']
        between_search = []
        like_search = []
        membership_search = []
        for key, value in filters.items():

            col = args_mapper[key]

            if key == "search":
                value = value.strip()
                or_conditions = [column.like(f"%{value}%") for column in col]
                custom_condition = or_(*or_conditions)
                filter_clause.append(custom_condition)


            if key in exact_search:
                filter_clause.append(col == value)

            if key in between_search:
                from_ = value.get("from", None)
                to_ = value.get("to", None)
                if from_ and to_:
                    filter_clause.append(args_mapper[key].between(from_, to_))
            if key in like_search:
                filter_clause.append(col.like(f"%{value}%"))
            if key in membership_search:

                if isinstance(value, list):
                    filter_clause.append(col.in_(value))
                else:
                    filter_clause.append(col.in_([value]))

        if filter_clause:
            query = query.filter(*filter_clause)

        customer_ls = db.execute(query).all()

        customer_list = []
        for customer in customer_ls:
            customer_list.append({
                "customer_name" : customer.customer_name,
                "status": customer.status,
                "customer_id": customer.customer_id
            })
        return customer_list

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e