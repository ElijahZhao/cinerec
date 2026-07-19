/**
 * CineRec — GSAP Animations + Lenis Smooth Scroll
 */
const Animations = (() => {
    let lenis = null;

    function initLenis() {
        if (typeof Lenis === 'undefined') return;
        lenis = new Lenis({
            duration: 1.2,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
            smooth: true,
        });
        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);
    }

    function initLoginAnimations() {
        // Split text animation for hero title
        if (typeof gsap === 'undefined') return;
        gsap.registerPlugin(ScrollTrigger);

        // Title entrance
        const titleLine = document.querySelector('.title-line');
        if (titleLine) {
            gsap.from(titleLine, {
                y: 60, opacity: 0, duration: 0.8, ease: 'power3.out', delay: 0.2
            });
        }

        // Subtitle entrance
        const subtitleLine = document.querySelector('.subtitle-line');
        if (subtitleLine) {
            gsap.from(subtitleLine, {
                y: 40, opacity: 0, duration: 0.8, ease: 'power3.out', delay: 0.4
            });
        }

        // Description fade in
        const desc = document.querySelector('.hero-desc');
        if (desc) {
            gsap.from(desc, {
                y: 20, opacity: 0, duration: 0.6, ease: 'power2.out', delay: 0.6
            });
        }

        // Login card slide up
        const loginCard = document.querySelector('.login-card');
        if (loginCard) {
            gsap.from(loginCard, {
                y: 80, opacity: 0, duration: 0.8, ease: 'power3.out', delay: 0.5
            });
        }

        // Algorithm steps stagger entrance
        const algoSteps = document.querySelectorAll('.algo-step');
        if (algoSteps.length) {
            gsap.from(algoSteps, {
                y: 20, opacity: 0, duration: 0.4, stagger: 0.15,
                ease: 'power2.out', delay: 0.8
            });
        }
    }

    function animateMovieCards() {
        if (typeof gsap === 'undefined') return;
        const cards = document.querySelectorAll('.movie-card');
        if (!cards.length) return;

        gsap.from(cards, {
            y: 40, opacity: 0, duration: 0.4, stagger: 0.05,
            ease: 'power2.out', clearProps: 'all'
        });
    }

    function animateRecCards() {
        if (typeof gsap === 'undefined') return;
        const cards = document.querySelectorAll('.rec-card');
        if (!cards.length) return;

        gsap.from(cards, {
            y: 50, opacity: 0, scale: 0.95, duration: 0.5, stagger: 0.08,
            ease: 'power3.out', clearProps: 'all'
        });
    }

    function countUp(element, target, duration = 1.5) {
        if (typeof gsap === 'undefined') { element.textContent = target.toFixed(4); return; }
        const obj = { val: 0 };
        gsap.to(obj, {
            val: target, duration: duration, ease: 'power2.out',
            onUpdate: () => { element.textContent = obj.val.toFixed(4); }
        });
    }

    function init() {
        initLenis();
        initLoginAnimations();
    }

    return { init, animateMovieCards, animateRecCards, countUp };
})();

document.addEventListener('DOMContentLoaded', () => Animations.init());