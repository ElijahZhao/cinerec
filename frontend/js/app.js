/**
 * CineRec — SPA Router, State Management, and i18n
 */
const CineRec = (() => {
    // State
    const state = {
        currentPage: 'login',
        userId: null,
        username: null,
        lang: 'en',
        apiBase: window.location.origin,
        movies: [],
        recommendations: [],
        currentAlgo: 'MultiModalNCF',
        moviePage: 1,
    };

    // i18n
    let i18nData = { en: {}, zh: {} };

    async function loadI18n() {
        try {
            const [enRes, zhRes] = await Promise.all([
                fetch('assets/i18n/en.json'),
                fetch('assets/i18n/zh.json')
            ]);
            i18nData.en = await enRes.json();
            i18nData.zh = await zhRes.json();
        } catch (e) {
            console.warn('Failed to load i18n:', e);
        }
    }

    function t(key) {
        const keys = key.split('.');
        let val = i18nData[state.lang];
        for (const k of keys) {
            val = val?.[k];
        }
        return val || key;
    }

    function applyI18n() {
        document.querySelectorAll('[data-i18n]').forEach(el => {
            el.textContent = t(el.dataset.i18n);
        });
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            el.placeholder = t(el.dataset.i18nPlaceholder);
        });
        document.getElementById('lang-label').textContent = state.lang.toUpperCase();
    }

    function toggleLang() {
        state.lang = state.lang === 'en' ? 'zh' : 'en';
        applyI18n();
    }

    // Navigation
    function navigateTo(page) {
        state.currentPage = page;
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        const pageEl = document.getElementById(`page-${page}`);
        const linkEl = document.querySelector(`.nav-link[data-page="${page}"]`);
        if (pageEl) pageEl.classList.add('active');
        if (linkEl) linkEl.classList.add('active');

        // Trigger page-specific animations
        if (page === 'recommend') loadRecommendations();
        if (page === 'dashboard') loadDashboard();
        if (page === 'movies' && state.movies.length === 0) loadMovies();

        // Scroll to top
        window.scrollTo(0, 0);
    }

    // Auth state
    function setUser(userId, username) {
        state.userId = userId;
        state.username = username;
        const badge = document.getElementById('user-badge');
        const nameEl = document.getElementById('user-name');
        badge.classList.remove('hidden');
        nameEl.textContent = username;
        navigateTo('recommend');
    }

    // API helper
    async function api(path, options = {}) {
        const url = `${state.apiBase}${path}`;
        try {
            const res = await fetch(url, options);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return await res.json();
        } catch (e) {
            console.error(`API Error [${path}]:`, e);
            throw e;
        }
    }

    // Init
    async function init() {
        await loadI18n();
        applyI18n();

        // Nav clicks
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                navigateTo(link.dataset.page);
            });
        });

        // Lang toggle
        document.getElementById('lang-toggle').addEventListener('click', toggleLang);

        // Load genre filter
        try {
            const genresData = await api('/api/movies/genres');
            const select = document.getElementById('genre-filter');
            genresData.genres.forEach(g => {
                const opt = document.createElement('option');
                opt.value = g;
                opt.textContent = g;
                select.appendChild(opt);
            });
        } catch (e) {
            console.warn('Could not load genres');
        }
    }

    return { state, t, navigateTo, setUser, api, init, applyI18n };
})();

document.addEventListener('DOMContentLoaded', () => CineRec.init());