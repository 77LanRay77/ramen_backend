from fastapi import FastAPI
from pydantic import Field, BaseModel
import datetime

app = FastAPI()

class FormResults(BaseModel):
    p1: int = Field(lt=6, gt=0)
    p2: int = Field(lt=6, gt=0)
    p3: int = Field(lt=6, gt=0)
    p4: int = Field(lt=6, gt=0)
    p5: int = Field(lt=6, gt=0)
    p6: int = Field(lt=6, gt=0)

class Shop(BaseModel):
    name: str
    address: str
    phone: str
    opening_hours: datetime.time
    closing_hours: datetime.time
    rate: float

ramen_shops: list[Shop] = []

from fastapi import APIRouter, Form
from typing import Annotated

router = APIRouter()

@router.post("/form")
def submit_form(data: Annotated[FormResults, Form()]):
    data
    pass