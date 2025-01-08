from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "654a27b3ef9977ec30dffb81aae7e629"
BASE_URL = "https://api.themoviedb.org/3"
favorites = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_movies', methods=['GET'])
def get_movies():
    url = f"{BASE_URL}/discover/movie?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json().get('results', []))
    return jsonify({"error": "Failed to fetch movies"}), 500

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query is required"}), 400
    url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json().get('results', []))
    return jsonify({"error": "Failed to fetch search results"}), 500

@app.route('/favorites', methods=['GET', 'POST'])
def manage_favorites():
    global favorites
    if request.method == 'GET':
        return jsonify(favorites)
    elif request.method == 'POST':
        data = request.get_json()
        if 'id' in data:
            if any(fav['id'] == data['id'] for fav in favorites):
                favorites = [fav for fav in favorites if fav['id'] != data['id']]
                return jsonify({"message": f"Removed {data['title']} from favorites"}), 200
            favorites.append(data)
            return jsonify({"message": f"Added {data['title']} to favorites"}), 201
        return jsonify({"error": "Invalid data"}), 400

def get_similar_movies(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/similar?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    recommended = []
    seen_movie_ids = set()
    for fav in favorites:
        similar_movies = get_similar_movies(fav['id'])
        for movie in similar_movies:
            movie_id = movie['id']
            if movie_id not in seen_movie_ids and movie_id not in [f['id'] for f in favorites]:
                recommended.append(movie)
                seen_movie_ids.add(movie_id)
    recommended.sort(key=lambda x: x.get('popularity', 0), reverse=True)
    return jsonify(recommended)

if __name__ == "__main__":
    app.run(debug=True)
