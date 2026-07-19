/**
 * CineRec — Recommendations Page Logic
 */
async function loadRecommendations() {
    if (!CineRec.state.userId) {
        CineRec.navigateTo('login');
        return;
    }

    const algo = CineRec.state.currentAlgo;
    const recList = document.getElementById('rec-list');
    recList.innerHTML = '<div class="loading-spinner"></div>';

    try {
        const data = await CineRec.api(
            `/api/recommend?user_id=${CineRec.state.userId}&algorithm=${algo}&top_k=10`
        );
        CineRec.state.recommendations = data.recommendations;
        renderRecommendations(data.recommendations, algo);
        Animations.animateRecCards();
    } catch (err) {
        recList.innerHTML = `<p>${CineRec.t('common.error')}</p>`;
    }
}

function renderRecommendations(recs, algo) {
    const recList = document.getElementById('rec-list');
    if (!recs || !recs.length) {
        recList.innerHTML = `<p class="empty-state">${CineRec.t('rec.noRec')}</p>`;
        return;
    }

    recList.innerHTML = recs.map((rec, idx) => `
        <div class="rec-card spotlight-card glass-card" style="--delay: ${idx * 0.05}s">
            <div class="rec-rank">${idx + 1}</div>
            <div class="rec-poster">
                ${rec.poster_url
                    ? `<img src="${rec.poster_url}" alt="${rec.title}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=\\'poster-placeholder\\'><span>${rec.title?.charAt(0) || '?'}</span></div>'">`
                    : `<div class="poster-placeholder"><span>${rec.title?.charAt(0) || '?'}</span></div>`}
            </div>
            <div class="rec-info">
                <h3 class="rec-title">${rec.title}</h3>
                <div class="rec-meta">
                    ${rec.release_year ? `<span>${rec.release_year}</span>` : ''}
                    ${rec.genres ? `<span class="rec-genres">${rec.genres.split('|').slice(0, 3).join(' · ')}</span>` : ''}
                </div>
                <div class="rec-score">
                    <span class="score-label">${CineRec.t('rec.score')}:</span>
                    <span class="score-value" data-count="${rec.score}">${rec.score.toFixed(4)}</span>
                </div>
                <div class="rec-reasons">
                    ${(rec.reasons || []).map(r => `
                        <div class="reason-tag ${r.type}">
                            <span class="reason-icon">${r.type === 'collaborative' ? '👥' : r.type === 'content' ? '🎬' : r.type === 'genre_match' ? '🏷️' : '✨'}</span>
                            <span class="reason-text">${CineRec.state.lang === 'zh' ? (r.reason_zh || r.reason) : (r.reason_en || r.reason)}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `).join('');

    // CountUp animation for scores
    document.querySelectorAll('.score-value[data-count]').forEach(el => {
        Animations.countUp(el, parseFloat(el.dataset.count));
    });

    if (typeof Effects !== 'undefined') Effects.refresh();
}

document.addEventListener('DOMContentLoaded', () => {
    // Algorithm switcher
    document.querySelectorAll('.algo-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            document.querySelectorAll('.algo-chip').forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            CineRec.state.currentAlgo = chip.dataset.algo;
            loadRecommendations();
        });
    });

    // Refresh button
    document.getElementById('btn-refresh-rec').addEventListener('click', loadRecommendations);
});
