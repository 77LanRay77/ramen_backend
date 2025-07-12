from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import Annotated, List, Optional
import json
from example.analysis import analysis  # Import the analysis function
from match.store import match_store  # Import the match_store function

app = FastAPI()

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

