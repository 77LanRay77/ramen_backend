from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json

def anal(form) -> tuple[float, str, str]:
    with open("ramen_data.json", "r") as file:
        data = json.load(file)

    features = ['sweet', 'sour', 'spicy', 'salty', 'umami']
    # Define the target vector based on form input
    # Assuming 'form' is a dictionary with keys matching 'features'
    sigma_vector = np.array([[form[feat] for feat in features]])

    # Create the matrix of ramen vectors
    vectors = np.array([[r[feat] for feat in features] for r in data])

    # Calculate cosine similarity between the target vector and all ramen vectors
    # cosine_similarity returns a 2D array, so we take the first row [0]
    similarity_scores = cosine_similarity(sigma_vector, vectors)[0]

    # Calculate recommendation scores
    recommendation_score = ((similarity_scores + 1) / 2) * 100

    # Find the best recommendation based on the highest score
    best_index = np.argmax(recommendation_score)
    best_score = recommendation_score[best_index]
    best_name = data[best_index]['name']
    best_shop = data[best_index]['shop']

    return best_score, best_name, best_shop

