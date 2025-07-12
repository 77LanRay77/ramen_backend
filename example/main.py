from fastapi import FastAPI, Form, Field
from pydantic import BaseModel
from typing import Annotated, List, Optional

app = FastAPI()

class FormResults(BaseModel):
    name: str                      # Name of the ramen bowl
    shop_name: Optional[str]       # Optional: name of the restaurant/shop
    price: int                     # Price in local currency (e.g., NT$, ¥)
    available: bool = True         # Optional: whether it's currently available

    # Classification
    broth_type: str                # e.g., "tonkotsu", "shoyu", "miso"
    tags: List[str] = []           # e.g., ["fusion", "authentic", "comfort food"]
    toppings: List[str] = []       # e.g., ["egg", "chashu", "seaweed", "corn"]
    contains: List[str] = []       # ingredients that might be dietary restrictions (e.g., ["pork", "gluten"])

    # Taste Profile (1–5 scale)
    sweetness: int                 # 1 (not sweet) to 5 (very sweet)
    sourness: int
    spiciness: int
    saltiness: int
    bitterness: Optional[int] = 0  # Optional; not common in ramen
    umami: int

    # Texture & Body (1–5 scale)
    noodle_hardness: int           # 1 (very soft) to 5 (very hard)
    noodle_thickness: int          # 1 (very thin) to 5 (very thick)
    soup_thickness: int            # 1 (watery) to 5 (rich & creamy)

    # Meta Ratings
    rating: Optional[float] = None  # e.g., average user score (1–5)

    # Dining Context (Optional)
    context: Optional[str] = None 

@app.post("/form")
def submit_form(data: Annotated[FormResults, Form()]):
    return data

class Ramen(BaseModel):
    # Basic Info
    name: str                      # Name of the ramen bowl
    shop_name: Optional[str]       # Optional: name of the restaurant/shop
    price: int                     # Price in local currency (e.g., NT$, ¥)
    available: bool = True         # Optional: whether it's currently available

    # Classification
    broth_type: str                # e.g., "tonkotsu", "shoyu", "miso"
    tags: List[str] = []           # e.g., ["fusion", "authentic", "comfort food"]
    toppings: List[str] = []       # e.g., ["egg", "chashu", "seaweed", "corn"]
    contains: List[str] = []       # ingredients that might be dietary restrictions (e.g., ["pork", "gluten"])

    # Taste Profile (1–5 scale)
    sweetness: int                 # 1 (not sweet) to 5 (very sweet)
    sourness: int
    spiciness: int
    saltiness: int
    bitterness: Optional[int] = 0  # Optional; not common in ramen
    umami: int

    # Texture & Body (1–5 scale)
    noodle_hardness: int           # 1 (very soft) to 5 (very hard)
    noodle_thickness: int          # 1 (very thin) to 5 (very thick)
    soup_thickness: int            # 1 (watery) to 5 (rich & creamy)

    # Meta Ratings
    rating: Optional[float] = None  # e.g., average user score (1–5)

    # Dining Context (Optional)
    context: Optional[str] = None   # e.g., "solo", "date", "family", "late-night"


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

