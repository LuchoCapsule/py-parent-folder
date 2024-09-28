from pydantic import BaseModel
from typing import Optional
from interfaces.IUser import IUser  # Correct import

class IResponseStatus(BaseModel):
    status: str
    data: IUser