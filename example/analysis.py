import numpy as np
import json

def analysis(form) -> tuple[float, str, str]:
    with open("ramen_data.json", "r") as file:
        data = json.load(file)

    features = ['sweet', 'sour', 'spicy', 'salty', 'umami']
    # Define the target vector based on form input
    # Assuming 'form' is a dictionary with keys matching 'features'
    sigma_vector = np.array([form[feat] for feat in features]) # 將外層的 [] 移除，使其成為一維向量

    # Create the matrix of ramen vectors
    vectors = np.array([[r[feat] for feat in features] for r in data])

    # Calculate dot product between sigma_vector and each ramen vector
    dot_products = np.dot(vectors, sigma_vector)

    # Calculate the norm (magnitude) of sigma_vector
    norm_sigma = np.linalg.norm(sigma_vector)

    # Calculate the norm of each ramen vector
    norm_vectors = np.linalg.norm(vectors, axis=1)

    # Calculate cosine similarity: dot_product / (norm_sigma * norm_vector)
    # Handle potential division by zero if a vector has zero norm
    # Add a small epsilon to the denominator to avoid division by zero, or use nan_to_num
    denominator = norm_sigma * norm_vectors
    similarity_scores = np.where(denominator != 0, dot_products / denominator, 0.0)

    # Calculate recommendation scores
    recommendation_score = ((similarity_scores + 1) / 2) * 100

    # Find the best recommendation based on the highest score
    best_index = np.argmax(recommendation_score)
    best_score = recommendation_score[best_index]
    best_name = data[best_index]['name']
    best_shop = data[best_index]['shop']

    return best_score, best_name, best_shop

