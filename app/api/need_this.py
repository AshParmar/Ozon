import os
import numpy as np
import pandas as pd
from chatgpt import get_embeddings  # Import from the first file
from app.services import get_all_course_names, bulk_insert_embeddings, get_all_course_embeddings

# Define paths
assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
csv_path = os.path.join(assets_dir, 'Coursera.csv')

class Recommender:
    def __init__(self, path=csv_path):
        self.path = path
        self._load_embeddings()

    def _load_embeddings(self):
        """
        Load embeddings for courses from the CSV file and insert new embeddings into the database.
        """
        existing_course_names = set(get_all_course_names())
        data = pd.read_csv(self.path)
        embeddings_to_insert = []

        for course_name in data['course_name']:
            if course_name not in existing_course_names:
                embedding = get_embeddings(course_name)
                if embedding is not None:
                    embeddings_to_insert.append({'course_name': course_name, 'embedding': embedding})

        if embeddings_to_insert:
            bulk_insert_embeddings(embeddings_to_insert)

    def get_similarity_score(self, embedding1, embedding2):
        """
        Calculate the cosine similarity between two embeddings.
        """
        return np.inner(embedding1, embedding2)

    def get_recommendation(self, user_prompt, similarity_score_threshold=0.5, top_n=5):
        """
        Get course recommendations based on user input.
        """
        user_embedding = get_embeddings(user_prompt)
        if user_embedding is None:
            return []

        all_embeddings = get_all_course_embeddings()

        recommendations = [
            (course.course_name, self.get_similarity_score(user_embedding, course.embedding_list))
            for course in all_embeddings
            if self.get_similarity_score(user_embedding, course.embedding_list) >= similarity_score_threshold
        ]

        recommendations.sort(key=lambda x: -x[1])
        return recommendations[:top_n]

# Example usage
if __name__ == '__main__':
    recommender = Recommender()
    course = 'Natural language processing'
    recommendations = recommender.get_recommendation(course)
    print(recommendations)