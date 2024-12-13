"""
"""
from crud import CRUDBase
from models import CustomerQueueModel
from schemas.customer_queue import CustomerQueueSchema


class CRUDCustomerQueue(CRUDBase[CustomerQueueModel, CustomerQueueSchema, CustomerQueueSchema]):
    pass


CustomerQueue = CRUDCustomerQueue(CustomerQueueModel)
