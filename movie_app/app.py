import requests
from flask import Flask, jsonify, render_template, request
from config import ACCESS_TOKEN, API_BASE_URL, REDIRECT_URI, API_KEY

class MovieApp:
    def __init__(self, app=None):
        self.API_KEY = API_KEY
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.API_BASE_URL = API_BASE_URL
        self.REDIRECT_URI = REDIRECT_URI
        
        # Flask initialization
        if app is not None:
            self.app = app
            self.app.add_url_rule('/', 'index', self.index)
            self.app.add_url_rule('/home', 'home_route', self.home_route, methods=['GET', 'POST'])
            self.app.add_url_rule('/library', 'library_route', self.library_route)
            self.app.add_url_rule('/recommendations', 'recommendations_route', self.recommendations_route, methods=['GET', 'POST'])
            self.app.add_url_rule('/search_movie', 'search_movie', self.search_movie, methods=['GET', 'POST'])
            self.app.add_url_rule('/profile', 'profile_route', self.profile_route)
    
    # check Authentication
    def get_auth_status(self):
        url = f"{self.API_BASE_URL}authentication"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.ACCESS_TOKEN}"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("Authentication successful!")
            return response.json()
        else:
            print(f"Authentication failed! Status Code: {response.status_code}")
            print(response.text)
            return None
    
    def make_request(self, endpoint, params=None):
        url = f"{self.API_BASE_URL}{endpoint}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.ACCESS_TOKEN}"
        }

        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def search(self, query):
        file_path = f"search/movie?query={query}&include_adult=false&language=en-US&page=1"
        response = self.make_request(file_path)

        if response["results"]:
            return response["results"][0]
        else:
            return "No results found."

    def get_requirements_for_Recommendations(self, query):
        if not query:
            return []
        
        response = self.search(query)

        genres = response['genre_ids']
        vote_average = response['vote_average']
        # language = response['original_language']
        # release_date = response['release_date']
        # popularity = response['popularity']

        with_genres = ",".join(map(str, genres))
        vote_average_gte = vote_average - 0.5
        vote_average_lte = vote_average + 0.5
        # release_date_gte = release_date
        # release_date_lte = release_date

        url = f"discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&vote_average.gte={vote_average_gte}&vote_average.lte={vote_average_lte}&with_genres={with_genres}"

        movie_data = self.make_request(url)
        ids = [item["id"] for item in movie_data["results"]]

        base_url = "https://image.tmdb.org/t/p/w500"
        movie_images = []

        for movie_id in ids:
            movie_data = self.make_request(f"movie/{movie_id}")
            movie_image_data = self.make_request(f"movie/{movie_id}/images")

            if "backdrops" in movie_image_data and movie_image_data["backdrops"]:
                file_path = movie_image_data['backdrops'][0]['file_path']
                url = base_url + file_path
                movie_images.append({
                    "image_url": url,
                    "title": movie_data["title"],
                    "vote_average": movie_data["vote_average"]
                })

        return movie_images


    def get_movies_data(self, type):
        return self.make_request(f"movie/{type}")

    def get_ids_of_movie(self, type):
        movie_data = self.get_movies_data(type=type)
        ids = [item["id"] for item in movie_data["results"]]
        return ids

    def get_movie_images(self, type):
        base_url = "https://image.tmdb.org/t/p/w500"
        popular_movie_ids = self.get_ids_of_movie(type=type)

        movie_images = []

        for movie_id in popular_movie_ids:
            movie_data = self.make_request(f"movie/{movie_id}")
            movie_image_data = self.make_request(f"movie/{movie_id}/images")

            if "backdrops" in movie_image_data and movie_image_data["backdrops"]:
                file_path = movie_image_data['backdrops'][0]['file_path']
                url = base_url + file_path
                movie_images.append({
                    "image_url": url,
                    "title": movie_data["title"],
                    "vote_average": movie_data["vote_average"]
                })

        return movie_images
    

    # Flask route methods
    def index(self):
        return """
            Welcome to my Movie App 
            <a href='/home'>home</a>  
        """

    def home_route(self):
        category = "popular"
        if request.method == 'POST':
            category = request.form.get('button_value')
        result = self.get_movie_images(category)
        return render_template('home.html', result=result, category=category)

    def library_route(self):
        return render_template('library.html')

    def recommendations_route(self):
        query = request.form.get("query")
        result = self.get_requirements_for_Recommendations(query)
        return render_template('recommendations.html', result=result)

    def search_movie(self):
        query = request.json.get('query')
        if not query:
            return jsonify({"error": "Query is required"}), 400

        result = self.search(query)
        if isinstance(result, dict):
            return jsonify({
                "title": result.get("title"),
                "description": result.get("overview"),
                "image": f"https://image.tmdb.org/t/p/w200{result.get('poster_path')}",
                "user_rating": round(result.get("vote_average") / 2, 1)
            })
        else:
            return jsonify({"error": "Movie not found"}), 404

    def profile_route(self):
        return render_template('profile.html')

# Flask app initialization
app = Flask(__name__)
movie_app = MovieApp(app)

if __name__ == "__main__":

    app.run(debug=True)



