from flask import Flask, jsonify, render_template, request
from services import get_movie_images, get_popular_movies_data, search

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to my Movie App <a href='/home'> Login</a>"

@app.route('/home')
def home_route():
    result = get_movie_images()
    return render_template('home.html', result=result)

@app.route('/library')
def library_route():
    return render_template('library.html')


@app.route('/search_movie', methods=['POST'])
def search_movie():
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "Query is required"}), 400

    result = search(query)
    if isinstance(result, dict):
        return jsonify({
            "title": result.get("title"),
            "description": result.get("overview"),
            "image": f"https://image.tmdb.org/t/p/w200{result.get('poster_path')}",
            "user_rating": round(result.get("vote_average") / 2, 1)
        })
    else:
        return jsonify({"error": "Movie not found"}), 404

@app.route('/profile')
def profile_route():
    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=True)
