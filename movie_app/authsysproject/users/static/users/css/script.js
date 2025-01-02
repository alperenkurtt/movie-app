const API_URL = 'https://api.themoviedb.org/3/discover/movie?api_key=654a27b3ef9977ec30dffb81aae7e629';
const API_KEY = '654a27b3ef9977ec30dffb81aae7e629';
const IMG_PATH = 'https://image.tmdb.org/t/p/w200';
const SEARCH_URL = `https://api.themoviedb.org/3/search/movie?api_key=${API_KEY}&query=`;

const main = document.getElementById('main');
const form = document.getElementById('form');
const search = document.getElementById('search');

// Favoriler listesi (ID'ler yerine obje kullanabilirsiniz)
let favorites = JSON.parse(localStorage.getItem('favorites')) || [];

// İlk yüklemede filmleri getir
getMovies(API_URL);

// Filmleri getir ve göster
async function getMovies(url) {
    try {
        const res = await fetch(url);
        const data = await res.json();
        showMovies(data.results);
    } catch (error) {
        console.error('Filmleri çekerken hata oluştu:', error);
        main.innerHTML = '<h2>Filmleri yüklerken bir hata oluştu.</h2>';
    }
}

// Filmleri göstermek için fonksiyon
function showMovies(movies) {
    main.innerHTML = ''; // Eski içerikleri temizle
    movies.forEach((movie) => {
        const { id, title, poster_path, vote_average, overview } = movie;

        // Poster kontrolü yapıyoruz
        const poster = poster_path ? IMG_PATH + poster_path : 'https://via.placeholder.com/200x300?text=No+Image';

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
                <button class="favorite-btn" data-id="${id}">
                    ${favorites.some(fav => fav.id === id) ? 'Remove from Favourites' : 'Add to Favourites'}
                </button>
            </div>
        `;

        const favoriteBtn = movieEl.querySelector('.favorite-btn');
        favoriteBtn.addEventListener('click', () => toggleFavorite(movie));

        main.appendChild(movieEl);
    });
}

// Oy puanına göre sınıf döndüren fonksiyon
function getClassByRate(vote) {
    if (vote >= 8) {
        return 'green';
    } else if (vote >= 5) {
        return 'orange';
    } else {
        return 'red';
    }
}

// Favori ekleme/çıkarma fonksiyonu
function toggleFavorite(movie) {
    const { id, title } = movie;
    const existing = favorites.find(fav => fav.id === id);

    if (existing) {
        favorites = favorites.filter(fav => fav.id !== id);
        alert(`${title} Removed from Favourites.`);
    } else {
        favorites.push({ id, title });
        alert(`${title} Added to Favourites.`);
    }

    // Favorileri localStorage'a kaydet
    localStorage.setItem('favorites', JSON.stringify(favorites));

    // Filmleri yeniden göster (buton durumunu güncellemek için)
    getMovies(API_URL);
}

// Favoriler sayfasını göster
async function showFavorites() {
    main.innerHTML = ''; // Eski içerikleri temizle
    if (favorites.length === 0) {
        main.innerHTML = '<h2>Your favourite list is empty.</h2>';
        return;
    }

    try {
        const moviePromises = favorites.map(fav =>
            fetch(`https://api.themoviedb.org/3/movie/${fav.id}?api_key=${API_KEY}`)
                .then(res => res.json())
        );

        const favoriteMovies = await Promise.all(moviePromises);
        showMovies(favoriteMovies);
    } catch (error) {
        console.error('Favori filmleri çekerken hata oluştu:', error);
        main.innerHTML = '<h2>Favori filmleri yüklerken bir hata oluştu.</h2>';
    }
}

// Arama özelliği
form.addEventListener('submit', (e) => {
    e.preventDefault();

    const searchTerm = search.value.trim();

    if (searchTerm && searchTerm !== '') {
        getMovies(SEARCH_URL + encodeURIComponent(searchTerm));
        search.value = '';
    } else {
        getMovies(API_URL); // Boş arama yapıldığında ana sayfayı göster
    }
});

// "Favorilerim" butonu ekle
const favoritesButton = document.createElement('button');
favoritesButton.textContent = 'My Favourites';
favoritesButton.style.marginLeft = '10px';
favoritesButton.style.backgroundColor = 'var(--secondary-color)';
favoritesButton.style.color = '#fff';
favoritesButton.style.border = 'none';
favoritesButton.style.borderRadius = '50px';
favoritesButton.style.padding = '.5rem 1rem';
favoritesButton.style.fontFamily = 'inherit';
favoritesButton.style.cursor = 'pointer';
favoritesButton.addEventListener('click', showFavorites);
form.appendChild(favoritesButton);

// **"Ana Sayfa" Butonu Ekleme Bölümü Başlıyor**
// "Ana Sayfa" butonunu oluştur
const homeButton = document.createElement('button');
homeButton.textContent = 'Home';
homeButton.style.marginLeft = '10px';
homeButton.style.backgroundColor = 'var(--secondary-color)'; // "Favorilerim" butonuyla aynı renk
homeButton.style.color = '#fff';
homeButton.style.border = 'none';
homeButton.style.borderRadius = '50px';
homeButton.style.padding = '.5rem 1rem';
homeButton.style.fontFamily = 'inherit';
homeButton.style.cursor = 'pointer';

// "Ana Sayfa" butonuna tıklandığında ana sayfadaki filmleri göster
homeButton.addEventListener('click', () => {
    getMovies(API_URL);
});

// "Favorilerim" butonunun yanına "Ana Sayfa" butonunu ekle
form.appendChild(homeButton);
// **"Ana Sayfa" Butonu Ekleme Bölümü Bitişiyor**
