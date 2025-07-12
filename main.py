from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import Annotated, List, Optional
import json
from example.analysis import analysis  # Import the analysis function
from match.store import match_store  # Import the match_store function

app = FastAPI()


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

class FormResults(BaseModel):
    sweetness: int
    sourness: int
    spiciness: int
    saltiness: int
    umami: int

@app.post("/analyze")
def analyze_ramen(data: FormResults):
    # Convert the form data to a dictionary
    form_data = data.dict()

    # Call the analysis function
    best_score, best_name, best_shop = analysis(form_data)

    # Return the analysis results
    return {
        "best_score": best_score,
        "best_name": best_name,
        "best_shop": best_shop
    }

