from flask import Flask, jsonify, render_template, request, session, redirect
from services import get_movie_images, get_movie_images2, search
from config import USER_FILE, MOVIES_FILE
import pandas as pd
from datetime import datetime


app = Flask(__name__)
app.secret_key = "12345"

@app.route('/')
def index():
    return """
        Welcome to my Movie App 
        <a href='/home'>Home</a>  
        <a href='/login'>Login</a>
        <a href='/register'>Register</a>
    """

@app.route('/home')
def home_route():
    result = get_movie_images()
    return render_template('home.html', result=result)

@app.route('/home2')
def home_route2():
    result = get_movie_images2()
    return render_template('home2.html', result=result)

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


@app.route('/register', methods=['GET', 'POST'])
def register():
     if request.method == 'POST':
         username = request.form['username']
         password = request.form['password']
         email = request.form['email']


         try:
             users = pd.read_excel(USER_FILE, engine='openpyxl')
         except FileNotFoundError:
             users = pd.DataFrame(columns=['username', 'password', 'email'])

         if username in users['username']:
             return "Bu kullanıcı adı zaten var!"

         new_user = pd.DataFrame({'username': [username], 'password': [password], 'email': [email]})
         users = pd.concat([users, new_user], ignore_index=True)
         users.to_excel(USER_FILE, index=False, engine='openpyxl')
         return redirect('/login')

     return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
         username = request.form['username']
         password = request.form['password']

         try:
            users = pd.read_excel(USER_FILE, engine='openpyxl')
         except FileNotFoundError:
            return "Kullanıcı veritabanı bulunamadı!"

         if username in users['username'].values:
             user = users[users['username'] == username]
             if user['password'].values[0] == password:
                 session['username'] = username
                 return redirect('/dashboard')
             else:
                 return "Şifre yanlış!"
         else:
             return "Kullanıcı bulunamadı!"

     return render_template('login.html')



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
     if 'username' not in session:
         return redirect('/login')

     if request.method == 'POST':
         movie = request.form['movie']

         try:
             movies = pd.read_excel(MOVIES_FILE, engine='openpyxl')
         except FileNotFoundError:
             movies = pd.DataFrame(columns=['username', 'movie', 'date'])

         new_movie = pd.DataFrame({'username': [session['username']],
                                   'movie': [movie],
                                   'date': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]})
         movies = pd.concat([movies, new_movie], ignore_index=True)
         movies.to_excel(MOVIES_FILE, index=False, engine='openpyxl')


     try:
         movies = pd.read_excel(MOVIES_FILE, engine='openpyxl')
         user_movies = movies[movies['username'] == session['username']]
     except FileNotFoundError:
         user_movies = pd.DataFrame(columns=['movie', 'date'])

     return render_template('dashboard.html', movies=user_movies)



@app.route('/logout')
def logout():
     session.pop('username', None)
     return redirect('/login')


if __name__ == "__main__":
    app.run(debug=True)
