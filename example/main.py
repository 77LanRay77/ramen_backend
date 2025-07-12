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

class Ramen(BaseModel):
    name: str
    price: int
    party: str
    kind: str
    tabooos: list[str]
    sweetness: int
    sourness: int
    spiciness: int
    saltiness: int
    bitterness: int
    umami: int
    noodle_hardness: int
    soup_thickness: int

Ramen_list : list[Ramen] = []

@app.post("/ramen")
def create_ramen(ramen: Ramen) -> Ramen:
    Ramen_list.append(ramen)
    return ramen

@app.get("/ramen")
def get_ramen() -> list[Ramen]:
    return Ramen_list

@app.get("/ramen")
def get_ramen_by_name(name: str) -> Ramen:
    return [ramen for ramen in Ramen_list if ramen.name == name]

@app.put("/ramen/{name}")
def update_ramen(name: str, ramen: Ramen) -> Ramen:
    for i, r in enumerate(Ramen_list):
        if r.name == name:
            Ramen_list[i] = ramen
            return ramen
    return {"error": "Ramen not found"} 

@app.delete("/ramen/{name}")
def delete_ramen(name: str) -> list[Ramen]:
    global Ramen_list
    Ramen_list = [ramen for ramen in Ramen_list if ramen.name != name]
    return Ramen_list