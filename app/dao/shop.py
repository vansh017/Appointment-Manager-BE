import bcrypt
from sqlalchemy.orm import Session

import crud
from models import UserModel
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