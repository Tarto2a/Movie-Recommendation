from flask import Flask, render_template, request
from spellchecker import SpellChecker
import pandas as pd
from ..data.loader import load_processed_data
from ..models.recommend import recommend_movies, limit_dataset_size

app = Flask(__name__)

# Initialize SpellChecker
spell = SpellChecker()

# Function for spelling correction
def correct_spelling(user_input):
    words = user_input.split()  # Split the input into words
    corrected_words = [spell.correction(word) for word in words]  # Correct each word
    return " ".join(corrected_words)  # Return the corrected sentence

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    if request.method == "POST":
        user_description = request.form["description"]
        corrected_description = correct_spelling(user_description)
        top_n = int(request.form["top_n"])
        movie_data = load_processed_data()

        if movie_data.empty:  # Check if DataFrame is empty
            return "Error loading movie data or data is empty."

        # Limit the dataset size before passing it to the recommendation function
        movie_data = limit_dataset_size(movie_data, sample_size=20000)

        recommendations = recommend_movies(corrected_description, movie_data, top_n)
    

    # Debugging: print recommendations to see its structure
    print(recommendations)  # Check the structure of recommendations

    if isinstance(recommendations, list) and len(recommendations) > 0:
        return render_template("index.html", recommendations=recommendations)
    elif isinstance(recommendations, pd.DataFrame) and not recommendations.empty:
        return render_template("index.html", recommendations=recommendations.to_dict(orient='records'))
    else:
        return render_template("index.html", recommendations=[])

if __name__ == "__main__":
    app.run(debug=True)
