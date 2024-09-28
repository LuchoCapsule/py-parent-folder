from pydantic import BaseModel
from typing import Optional

class IUser(BaseModel):
    id: Optional[int] = None
    name: str
    username: str
    email: str