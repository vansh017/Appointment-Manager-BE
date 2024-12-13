from typing import List

import bcrypt
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import Session

import crud
from models import UserModel, ShopMasterModel, UserShopModel, AddressModel, CatalogModel
from schemas import ShopSchema, CatalogSchema
from schemas.api_schemas import CreateShop
from core import TSServerError, get_current_date_time, api_log


def create_shop(db: Session, shop_details : CreateShop, user : UserModel):
    """

    :param db:
    :param shop_details:
    :param user:
    :return:
    """

    try:

        contact = crud.ContactDetails.create(db=db, record=shop_details.contact_details)
        address = crud.Address.create(db=db, record=shop_details.address)

        shop_obj = ShopSchema(
            shop_name = shop_details.shop_name,
            start_time = shop_details.start_time,
            end_time = shop_details.end_time,
            address_id = address.id,
            contact_id = contact.id
        )

        shop = crud.Shop.create(db=db, record=shop_obj)

        user_shop_obj = {"user_id": user.id, "shop_id": shop.id}

        user_shop = crud.UserShop.create(db=db, record=user_shop_obj)

        for item in shop_details.catalog_list:
            item.shop_id = shop.id

        catalog_list = crud.Catalog.add_multiple_records(db=db,objects=shop_details.catalog_list )

        return shop

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e


def create_shop_menu(db: Session, menu_details : List[CatalogSchema], user : UserModel):
    """

    :param db:
    :param menu_details:
    :param user:
    :return:
    """

    try:

        crud.Catalog.add_multiple_records(db=db,objects=menu_details)

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e


def get_shops(db:Session, filters : dict = None, sort_fields: list = None, paginate: dict = None):
    """

    :param db:
    :param filters:
    :param sort_fields:
    :param paginate:
    :return:
    """
    try:
        if not sort_fields:
            sort_fields = []

        if not filters:
            filters = {}
        query = (select(ShopMasterModel.id,
                        ShopMasterModel.shop_name,
                        ShopMasterModel.end_time,
                        AddressModel.address_line_1,
                        AddressModel.address_line_2,
                        AddressModel.city,
                        AddressModel.state,
                        AddressModel.zipcode,
                        UserModel.email,
                        func.concat(UserModel.first_name," ", UserModel.last_name).label("owner_name"))
                 .join(UserShopModel, and_(UserShopModel.shop_id == ShopMasterModel.id))
                 .join(UserModel, and_(UserShopModel.user_id == UserModel.id))
                 .join(AddressModel, and_(AddressModel.id == ShopMasterModel.address_id))
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

        shop_ls = db.execute(query).all()

        shop_list = []
        for shop in shop_ls:
            shop_list.append(shop._asdict())
        return shop_list

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e


def get_shop_menu(db:Session,  shop_id :int ,  filters : dict = None, sort_fields: list = None,paginate: dict = None):
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
        query = select(CatalogModel).where(CatalogModel.shop_id == shop_id)

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

        menu_ls = db.execute(query).all()

        menu_list = []
        for menu in menu_ls:
            menu = menu[0]
            menu_list.append({
                "item_name": menu.item_name,
                "expected_time": menu.expected_time,
                "price": menu.price
            })
        return menu_list

    except TSServerError as e:
        raise e

    except Exception as e:
        raise e