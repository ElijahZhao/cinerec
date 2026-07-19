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
            const card = e.target.closest('.movie-card, .rec-card');
            if (!card) return;
            const rect = card.getBoundingClientRect();
            card.style.setProperty('--mouse-x', (e.clientX - rect.left) + 'px');
            card.style.setProperty('--mouse-y', (e.clientY - rect.top) + 'px');
        });

        // Click Spark
        document.addEventListener('click', (e) => {
            const spark = document.createElement('div');
            spark.className = 'spark';
            spark.style.left = e.clientX + 'px';
            spark.style.top = e.clientY + 'px';

            for (let i = 0; i < 8; i++) {
                const particle = document.createElement('div');
                particle.className = 'spark-particle';
                const angle = (Math.PI * 2 * i) / 8 + (Math.random() - 0.5) * 0.5;
                const distance = 20 + Math.random() * 30;
                particle.style.setProperty('--dx', Math.cos(angle) * distance + 'px');
                particle.style.setProperty('--dy', Math.sin(angle) * distance + 'px');
                spark.appendChild(particle);
            }

            document.body.appendChild(spark);
            setTimeout(() => spark.remove(), 700);
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