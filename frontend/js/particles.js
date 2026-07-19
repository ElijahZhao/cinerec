/**
 * CineRec — tsParticles Star Field Background
 */
const Particles = (() => {
    async function init() {
        if (typeof tsParticles === 'undefined') return;

        const container = document.getElementById('particles-bg');
        if (!container) return;

        await tsParticles.load("particles-bg", {
            fullScreen: false,
            fpsLimit: 60,
            particles: {
                number: { value: 80, density: { enable: true, area: 900 } },
                color: { value: ["#d4a843", "#4a9eff", "#ffffff"] },
                shape: { type: "circle" },
                opacity: {
                    value: { min: 0.1, max: 0.5 },
                    animation: { enable: true, speed: 0.5, sync: false }
                },
                size: {
                    value: { min: 0.5, max: 2 },
                    animation: { enable: true, speed: 1, sync: false }
                },
                move: {
                    enable: true,
                    speed: 0.3,
                    direction: "none",
                    random: true,
                    straight: false,
                    outModes: "out"
                },
                links: {
                    enable: true,
                    distance: 150,
                    color: "#ffffff",
                    opacity: 0.08,
                    width: 0.5
                }
            },
            detectRetina: true,
            interactivity: {
                events: {
                    onHover: { enable: true, mode: "grab" },
                    onClick: { enable: true, mode: "push" }
                },
                modes: {
                    grab: { distance: 200, links: { opacity: 0.3 } },
                    push: { quantity: 2 }
                }
            }
        });
    }

    return { init };
})();

document.addEventListener('DOMContentLoaded', () => Particles.init());