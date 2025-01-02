import requests

url = "https://api.themoviedb.org/3/movie/912649/images"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NTRhMjdiM2VmOTk3N2VjMzBkZmZiODFhYWU3ZTYyOSIsIm5iZiI6MTczNDk2MDQ2NC43MzksInN1YiI6IjY3Njk2NTUwNWQ2ZTM2N2MyYjVjZjA3NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.sRlKCJmheIATr4nBKrrXsU41rlbIzv7sZ2yxz0xpjNI"
}

response = requests.get(url, headers=headers)

print(response.text)