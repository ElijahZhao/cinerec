/**
 * CineRec — Movie Browsing Page Logic
 */
async function loadMovies(page = 1) {
    const search = document.getElementById('movie-search').value;
    const genre = document.getElementById('genre-filter').value;
    const sort = document.getElementById('sort-select').value;

    try {
        const data = await CineRec.api(
            `/api/movies?page=${page}&per_page=20&search=${encodeURIComponent(search)}&genre=${encodeURIComponent(genre)}&sort=${sort}`
        );
        CineRec.state.movies = data.movies;
        renderMovieGrid(data.movies);
        renderPagination(data.page, data.pages);
        Animations.animateMovieCards();
    } catch (err) {
        document.getElementById('movies-grid').innerHTML = `<p>${CineRec.t('common.error')}</p>`;
    }
}

function renderMovieGrid(movies) {
    const grid = document.getElementById('movies-grid');
    if (!movies.length) {
        grid.innerHTML = `<p class="empty-state">${CineRec.t('movies.noResults')}</p>`;
        return;
    }

    grid.innerHTML = movies.map(m => `
        <div class="movie-card tilt-card spotlight-card" data-id="${m.id}">
            <div class="movie-poster">
                ${m.poster_url
                    ? `<img src="${m.poster_url}" alt="${m.title}" loading="lazy" onerror="this.src=''">`
                    : `<div class="poster-placeholder"><span>${m.title?.charAt(0) || '?'}</span></div>`}
            </div>
            <div class="movie-info">
                <h3 class="movie-title">${m.title}</h3>
                <div class="movie-meta">
                    ${m.release_year ? `<span class="movie-year">${m.release_year}</span>` : ''}
                    ${m.genres ? `<span class="movie-genres">${m.genres.split('|').slice(0, 3).join(' · ')}</span>` : ''}
                </div>
                <div class="movie-actions">
                    <button class="btn-sm btn-outline" onclick="openRatingModal(${m.id}, '${(m.title || '').replace(/'/g, "\\'")}')">
                        ${CineRec.t('movies.rate')}
                    </button>
                </div>
            </div>
        </div>
    `).join('');

    // Re-init effects for new cards
    if (typeof Effects !== 'undefined') Effects.refresh();
}

function renderPagination(current, total) {
    const pag = document.getElementById('movies-pagination');
    if (total <= 1) { pag.innerHTML = ''; return; }

    let html = '';
    for (let i = 1; i <= total; i++) {
        html += `<button class="page-btn ${i === current ? 'active' : ''}" onclick="loadMovies(${i})">${i}</button>`;
    }
    pag.innerHTML = html;
}

// Rating modal
let ratingMovieId = null;
function openRatingModal(movieId, title) {
    ratingMovieId = movieId;
    document.getElementById('rating-movie-title').textContent = title;
    document.getElementById('rating-modal').classList.remove('hidden');
    document.querySelectorAll('.star-rating .star').forEach(s => s.classList.remove('active'));
    Effects.refresh();
}

document.addEventListener('DOMContentLoaded', () => {
    // Close modal
    document.querySelector('.modal-close').addEventListener('click', () => {
        document.getElementById('rating-modal').classList.add('hidden');
    });
    document.getElementById('rating-modal').addEventListener('click', (e) => {
        if (e.target === e.currentTarget) e.currentTarget.classList.add('hidden');
    });

    // Star rating interaction
    const stars = document.querySelectorAll('.star-rating .star');
    let currentRating = 0;
    stars.forEach(star => {
        star.addEventListener('mouseenter', () => {
            const val = parseInt(star.dataset.value);
            stars.forEach(s => s.classList.toggle('active', parseInt(s.dataset.value) <= val));
        });
        star.addEventListener('click', () => {
            const val = parseInt(star.dataset.value);
            currentRating = val;
            stars.forEach(s => s.classList.toggle('active', parseInt(s.dataset.value) <= val));
        });
    });
    document.querySelector('.star-rating').addEventListener('mouseleave', () => {
        stars.forEach(s => s.classList.toggle('active', parseInt(s.dataset.value) <= currentRating));
    });

    // Submit rating
    document.getElementById('btn-submit-rating').addEventListener('click', () => {
        const activeStar = document.querySelector('.star-rating .star.active:last-of-type');
        if (!activeStar || !ratingMovieId) return;
        const rating = parseInt(activeStar.dataset.value);
        // Demo: just close modal
        document.getElementById('rating-modal').classList.add('hidden');
    });

    // Search with debounce
    let searchTimer;
    document.getElementById('movie-search').addEventListener('input', () => {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(() => loadMovies(1), 300);
    });

    // Filter changes
    document.getElementById('genre-filter').addEventListener('change', () => loadMovies(1));
    document.getElementById('sort-select').addEventListener('change', () => loadMovies(1));
});
