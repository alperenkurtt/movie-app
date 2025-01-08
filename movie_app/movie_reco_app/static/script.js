const API_URL = '/get_movies';
const SEARCH_URL = '/search?query=';
const main = document.getElementById('main');
const form = document.getElementById('form');
const search = document.getElementById('search');
const favoritesBtn = document.getElementById('favorites-btn');
const homeBtn = document.getElementById('home-btn');
const recommendationsBtn = document.getElementById('recommendations-btn');

// Favoriler listesini global olarak sakla
let favoriteIds = [];

// API'den filmleri çek ve göster
async function getMovies(url) {
    await loadFavorites(); // Favorileri güncel al
    const res = await fetch(url);
    const data = await res.json();
    showMovies(data);
}

// Filmleri göster
function showMovies(movies) {
    main.innerHTML = '';
    movies.forEach(movie => {
        const { id, title, poster_path, vote_average, overview } = movie;
        const poster = poster_path
            ? `https://image.tmdb.org/t/p/w200${poster_path}`
            : 'https://via.placeholder.com/200x300?text=No+Image';

        const movieEl = document.createElement('div');
        movieEl.classList.add('movie');
        movieEl.innerHTML = `
            <img src="${poster}" alt="${title}">
            <div class="movie-info">
                <h3>${title}</h3>
                <span class="${getClassByRate(vote_average)}">${vote_average}</span>
            </div>
            <div class="overview">
                <h3>Overview</h3>
                <p>${overview}</p>
                <button class="favorite-btn" data-id="${id}" data-title="${title}" data-poster="${poster_path}" data-overview="${overview}" data-vote="${vote_average}">
                    ${favoriteIds.includes(id) ? 'Remove from Favourites' : 'Add to Favourites'}
                </button>
            </div>
        `;
        const favBtn = movieEl.querySelector('.favorite-btn');
        favBtn.addEventListener('click', () => toggleFavorite(movie, favBtn));
        main.appendChild(movieEl);
    });
}

// Favori filmleri göster
async function showFavorites() {
    const res = await fetch('/favorites');
    const favorites = await res.json();
    favoriteIds = favorites.map(fav => fav.id); // Favori ID'leri güncelle
    showMovies(favorites);
}

// Oy puanına göre sınıf döndür
function getClassByRate(vote) {
    if (vote >= 8) return 'green';
    else if (vote >= 5) return 'orange';
    else return 'red';
}

// Favorilere ekleme/çıkarma
async function toggleFavorite(movie, button) {
    const { id, title, poster_path, overview, vote_average } = movie;
    const isFavorite = favoriteIds.includes(id);

    const res = await fetch('/favorites', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, title, poster_path, overview, vote_average }),
    });

    const message = await res.json();
    alert(message.message);

    if (isFavorite) {
        favoriteIds = favoriteIds.filter(favId => favId !== id);
        button.textContent = 'Add to Favourites';
        if (window.location.pathname === '/favorites') {
            button.closest('.movie').remove();
        }
    } else {
        favoriteIds.push(id);
        button.textContent = 'Remove from Favourites';
    }
}

// Favorileri güncel al
async function loadFavorites() {
    const res = await fetch('/favorites');
    const favorites = await res.json();
    favoriteIds = favorites.map(fav => fav.id);
}

// Önerileri göster
recommendationsBtn.addEventListener('click', showRecommendations);

async function showRecommendations() {
    const res = await fetch('/recommendations');
    const recommendations = await res.json();
    showMovies(recommendations);
}

// Ana sayfayı yükle
form.addEventListener('submit', (e) => {
    e.preventDefault();
    const searchTerm = search.value;
    if (searchTerm) {
        getMovies(`${SEARCH_URL}${encodeURIComponent(searchTerm)}`);
    } else {
        getMovies(API_URL);
    }
});

// Favoriler ve Home butonlarına tıklama
favoritesBtn.addEventListener('click', showFavorites);
homeBtn.addEventListener('click', () => getMovies(API_URL));

// Sayfa yüklendiğinde filmleri yükle
getMovies(API_URL);
