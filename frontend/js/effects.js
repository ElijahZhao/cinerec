/**
 * CineRec — Interaction Effects
 * Magnetic Button, 3D Tilt Cards, Spotlight Cards (event delegation)
 */
const Effects = (() => {
    let _delegatedInitialized = false;

    function initDelegatedEffects() {
        // Magnetic buttons
        document.addEventListener('mousemove', (e) => {
            const btn = e.target.closest('.magnetic-btn');
            if (!btn) return;
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            btn.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
        });
        document.addEventListener('mouseleave', (e) => {
            const btn = e.target.closest?.('.magnetic-btn');
            if (btn) btn.style.transform = '';
        }, true);

        // Tilt cards
        document.addEventListener('mousemove', (e) => {
            const card = e.target.closest('.tilt-card');
            if (!card) return;
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width;
            const y = (e.clientY - rect.top) / rect.height;
            card.style.transform = `perspective(600px) rotateY(${(x - 0.5) * 10}deg) rotateX(${-(y - 0.5) * 10}deg)`;
        });
        document.addEventListener('mouseleave', (e) => {
            const card = e.target.closest?.('.tilt-card');
            if (card) card.style.transform = '';
        }, true);

        // Spotlight cards
        document.addEventListener('mousemove', (e) => {
            const card = e.target.closest('.spotlight-card');
            if (!card) return;
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--spotlight-x', `${x}px`);
            card.style.setProperty('--spotlight-y', `${y}px`);
        });

        _delegatedInitialized = true;
    }

    function init() {
        initDelegatedEffects();
    }

    // Re-init for dynamically added elements
    // With event delegation, this is a no-op after the first call
    function refresh() {
        if (!_delegatedInitialized) {
            initDelegatedEffects();
        }
    }

    return { init, refresh };
})();

document.addEventListener('DOMContentLoaded', () => Effects.init());