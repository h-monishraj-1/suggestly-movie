from flask import Flask, request, jsonify, render_template
from movie_recommendation import MovieRecommender
import pandas as pd

app = Flask(__name__)

# Initialize movie recommender
movie_recommender = MovieRecommender("movies_list.pkl", "similarity.pkl")

movies_df = pd.read_pickle("movies_list.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend_movies", methods=["POST"])
def recommend_movies():
    data = request.json
    movie_title = data.get("movie_title", "")
    recommendations = movie_recommender.recommend(movie_title)
    return jsonify({"recommendations": recommendations})

@app.route("/get_titles", methods=["GET"])
def get_titles():
    query = request.args.get("q", "").lower()
    if not query:
        return jsonify({"titles": []})
    
    matching_titles = movies_df[movies_df['title'].str.lower().str.contains(query, na=False)]['title'].head(10).tolist()
    return jsonify({"titles": matching_titles})

if __name__ == "__main__":
    app.run(debug=True)
