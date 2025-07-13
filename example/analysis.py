import numpy as np
import json
import os

def analysis(form) -> list[dict]:
    script_dir = os.path.dirname(__file__)

    # Load ramen data (which is a list of ramen entries)
    ramen_file_path = os.path.join(script_dir, "ramen_data.json") # This file should contain the list of ramen
    with open(ramen_file_path, "r", encoding='utf-8') as file:
        ramen_data = json.load(file)

    # Load shop data (which is a dictionary with shop names as keys)
    shop_file_path = os.path.join(script_dir, "shop_data.json") # This file should contain the dictionary of shops
    with open(shop_file_path, "r", encoding='utf-8') as file:
        raw_shop_dict = json.load(file)
    
    shop_data_map = {}
    # Iterate over the items of the dictionary (shop name, details)
    # This assumes raw_shop_dict is a dictionary, which it is if ramen_shop.json is correctly named.
    for shop_name_zh, details in raw_shop_dict.items():
        shop_data_map[shop_name_zh] = {
            "name": details.get("店名", shop_name_zh),
            "address": details.get("地址", "N/A"),
            "phone": details.get("電話", "N/A"),
            "opening_time": details.get("營業時間", "N/A"),
            "closing_time": details.get("歇業時間", "N/A"),
            "rating": details.get("評分", "N/A")
        }

    # Your features list, assuming your form and ramen data support these
    features = ['sweetness', 'sourness', 'spiciness', 'saltiness', 'umami']
    
    user_vector = np.array([getattr(form, feat) for feat in features]).astype(float) 

    ramen_vectors = []
    for r in ramen_data:
        ramen_vector = []
        for feat in features:
            ramen_vector.append(r.get(feat, 0)) 
        ramen_vectors.append(ramen_vector)
    ramen_vectors = np.array(ramen_vectors).astype(float)

    dot_products = np.dot(ramen_vectors, user_vector)

    norm_user = np.linalg.norm(user_vector)

    norm_ramen = np.linalg.norm(ramen_vectors, axis=1)

    denominator = norm_user * norm_ramen
    
    similarity_scores = np.where(
        denominator > np.finfo(float).eps,
        dot_products / denominator,
        0.0
    )

    recommendation_scores = ((similarity_scores + 1) / 2) * 100

    top_indices = np.argsort(recommendation_scores)[-5:][::-1]

    top_recommendations = []
    for i in top_indices:
        ramen = ramen_data[i]
        # Make sure the 'shop' key in ramen.json matches a key in ramen_shop.json (e.g., "麵屋浩")
        shop_name = ramen['shop']
        
        shop_info = shop_data_map.get(shop_name, {})

        recommendation_entry = {
            "score": float(recommendation_scores[i]),
            "name": ramen['name'],
            "shop": shop_name,
            "price": ramen.get("price"),
            "address": ramen.get("address", shop_info.get("address", "N/A")),
        }
        
        top_recommendations.append(recommendation_entry)
    return top_recommendations