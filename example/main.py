from fastapi import FastAPI, Form, Field
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

class FormResults(BaseModel):
    p1: str
    p2: int = Field(lt=6, gt=0)
    p3: int = Field(lt=6, gt=0)
    p4: int = Field(lt=6, gt=0)
    p5: int = Field(lt=6, gt=0)
    p6: str

@app.post("/form")
def submit_form(data: Annotated[FormResults, Form()]):
    return data