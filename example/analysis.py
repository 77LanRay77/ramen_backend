# analysis.py
import numpy as np
import json

def analysis(form) -> list[dict]:
    with open("ramen_data.json", "r") as file:
        data = json.load(file)

    features = ['sweetness', 'sourness', 'spiciness', 'saltiness', 'umami']
    
    user_vector = np.array([getattr(form, feat) for feat in features]).astype(float) 

    ramen_vectors = np.array([[r[feat] for feat in features] for r in data]).astype(float)

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

    top_recommendations = [
        {
            "score": float(recommendation_scores[i]),
            "name": data[i]['name'],
            "shop": data[i]['shop']
        }
        for i in top_indices
    ]

    return top_recommendations