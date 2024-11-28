from pydantic import BaseModel


class AddressSchema(BaseModel):

    shop_name: str
    start_time : datetime.time
    end_time : datetime.time
    address :