from pydantic import BaseModel


class PydanticBase(BaseModel):
    class Config:
        orm_mode = True
        # use_enum_values = True  # setting this to true will use convert
        # enum values into their actual types
