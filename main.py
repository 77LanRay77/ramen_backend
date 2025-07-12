from fastapi import FastAPI, Form, HTTPException, status
from pydantic import Field, BaseModel
from typing import Annotated, List, Optional, Dict
from example.analysis import analysis  # Import the analysis function directly
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Ramen(BaseModel):
    # Taste Profile (1–5 scale)
    sweetness: int                 # 1 (not sweet) to 5 (very sweet)
    sourness: int
    spiciness: int
    saltiness: int
    umami: int

# 使用字典來儲存拉麵，以名稱作為鍵
Ramen_db: Dict[str, Ramen] = {}

# /form 路由可以使用 Ramen 模型
@app.post("/form")
def submit_form(form_data: Annotated[Ramen, Form()]):
    # Call the analysis function to get the top 5 recommendations
    top_recommendations = analysis(form_data)

    # Extract the shop names from the top recommendations
    ramen_shops = [recommendation["shop"] for recommendation in top_recommendations]

    # Return the list of ramen shops
    return {"ramen_shops": top_recommendations}

@app.post("/ramen", response_model=Ramen, status_code=status.HTTP_201_CREATED)
def create_ramen(ramen: Ramen) -> Ramen:
    if ramen.name in Ramen_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ramen with this name already exists")
    Ramen_db[ramen.name] = ramen
    return ramen

@app.get("/ramen", response_model=List[Ramen])
def get_all_ramen() -> List[Ramen]:
    # 返回字典中的所有值
    return list(Ramen_db.values())

# 修改路由以使用路徑參數 {name} 來取得特定拉麵
@app.get("/ramen/{name}", response_model=Ramen)
def get_ramen_by_name(name: str) -> Ramen:
    # 從字典中查找
    ramen = Ramen_db.get(name)
    if ramen is None:
        # 如果找不到，返回 404 錯誤
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ramen not found")
    return ramen

@app.put("/ramen/{name}", response_model=Ramen)
def update_ramen(name: str, ramen: Ramen) -> Ramen:
    if name not in Ramen_db:
        # 如果找不到，返回 404 錯誤
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ramen not found")
    # 更新字典中的項目
    Ramen_db[name] = ramen
    return ramen

@app.delete("/ramen/{name}", response_model=Dict[str, bool])
def delete_ramen(name: str) -> Dict[str, bool]:
    if name not in Ramen_db:
        # 如果找不到，返回 404 錯誤
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ramen not found")
    # 從字典中刪除項目
    del Ramen_db[name]
    return {"ok": True}


