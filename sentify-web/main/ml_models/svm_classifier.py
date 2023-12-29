import pickle
import pandas as pd
from .preprocessing import data_preprocessor, process_review
import time
import os

# Constants
SVM_MODEL_PATH = "ml_models/svm_model.pkl"
TFIDF_MODEL_PATH = "ml_models/tfidf_model.pkl"


def load_model(file_path):
    with open(file_path, "rb") as model_file:
        model = pickle.load(model_file)
    return model


tfidf_vectorizer = load_model(TFIDF_MODEL_PATH)
svm_model = load_model(SVM_MODEL_PATH)


def analyze_review(data):
    df = pd.DataFrame(data)

    start_time = time.time()
    clean_data = data_preprocessor(df)
    end_time = time.time()

    print(f"\nCleaning time: {end_time - start_time} seconds")

    tfidf_matrix = tfidf_vectorizer.transform(clean_data["review"])

    start_time = time.time()
    prediction = svm_model.predict(tfidf_matrix)
    end_time = time.time()
    print(f"\nClassification time: {end_time - start_time} seconds")

    df["label"] = prediction

    return df


def analyze_review_single(review):
    clean_review = process_review(review)
    tfidf_matrix = tfidf_vectorizer.transform([clean_review])
    prediction = svm_model.predict(tfidf_matrix)

    return prediction[0]
