from flask import Flask, render_template
from services import get_movie_images

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

@app.route('/profile')
def profile_route():
    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=True)
