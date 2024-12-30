import math

def calculate_stars(vote_average, max_rating=10):
    """
    Converts a vote average (out of max_rating) into a 5-star rating.

    Args:
        vote_average (float): The vote average of the movie.
        max_rating (int): The maximum rating scale (default is 10).

    Returns:
        str: Star representation of the rating (e.g., "⭐⭐⭐⭐⭐").
    """
    star_rating = (vote_average / max_rating) * 5
    full_stars = math.floor(star_rating)
    half_star = 0 if star_rating - full_stars < 0.5 else 1
    stars = "⭐" * full_stars + ("✨" if half_star else "")
    return stars

# Example film JSON data
film_data = {
    "title": "Fight Club",
    "vote_average": 2.433
}

# Convert vote_average to stars
stars = calculate_stars(film_data["vote_average"])

# Display the result
print(f"{film_data['title']}: {stars}")
