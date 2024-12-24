from auth import make_request
# from auth import get_auth_status

# auth_status = get_auth_status()
# if auth_status:
#     print("TMDB API baglantisi basarili!")

def get_popular_movies_data():
    return make_request("movie/popular?language=en-US&page=1")

def get_top_rated_movies_data():
    return make_request("movie/top_rated?language=en-US&page=1")

def get_ids_of_popular_movie():
    popular_movie_data = get_popular_movies_data()
    ids = [item["id"] for item in popular_movie_data["results"]]
    return ids

def get_ids_of_top_rated_movie():
    popular_movie_data = get_top_rated_movies_data()
    ids = [item["id"] for item in popular_movie_data["results"]]
    return ids

def get_movie_images():
    base_url = "https://image.tmdb.org/t/p/w500"
    popular_movie_ids = get_ids_of_popular_movie()

    movie_images = []

    for movie_id in popular_movie_ids:
        movie_image_data = make_request(f"movie/{movie_id}/images")

        if "backdrops" in movie_image_data and movie_image_data["backdrops"]:
            file_path = movie_image_data['backdrops'][0]['file_path']
            url = base_url + file_path
            movie_images.append(url)
        else:
            movie_images.append(None)

    return movie_images

def search(query):
    file_path = f"search/movie?query={query}&include_adult=false&language=en-US&page=1"

    response = make_request(file_path)

    if response["results"]:
        return response["results"][0]
    else:
        return "No results found."








































































