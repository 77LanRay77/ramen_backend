from fastapi import FastAPI, Form, HTTPException, status
from pydantic import Field, BaseModel
from typing import Annotated, List, Optional, Dict



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

# 使用字典來儲存拉麵，以名稱作為鍵
Ramen_db: Dict[str, Ramen] = {}

# /form 路由可以使用 Ramen 模型
@app.post("/form")
def submit_form(data: Annotated[Ramen, Form()]):
    # 您可以在這裡處理表單資料，例如將其儲存到資料庫或 Ramen_db
    # 這裡只是簡單地返回資料
    return data

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

