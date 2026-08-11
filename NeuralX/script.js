/* ============================= */
/* FAQ ACCORDION */
/* ============================= */

const faqItems = document.querySelectorAll(".faq-item");

faqItems.forEach((item) => {

    const question = item.querySelector(".faq-question");

    question.addEventListener("click", () => {

        faqItems.forEach((otherItem) => {

            if (otherItem !== item) {
                otherItem.classList.remove("open");
            }

        });

        item.classList.toggle("open");

    });

});


/* ============================= */
/* SCROLL REVEAL */
/* ============================= */

const revealElements = document.querySelectorAll(
    ".section-heading, .about-card, .track-card, .timeline-item, .prize-card"
);

const observer = new IntersectionObserver(
    (entries) => {

        entries.forEach((entry) => {

            if (entry.isIntersecting) {

                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";

            }

        });

    },
    {
        threshold: 0.15
    }
);


revealElements.forEach((element) => {

    element.style.opacity = "0";
    element.style.transform = "translateY(30px)";
    element.style.transition = "opacity 0.7s ease, transform 0.7s ease";

    observer.observe(element);

});


/* ============================= */
/* MOUSE PARALLAX */
/* ============================= */

const neuralVisual = document.querySelector(".neural-visual");

document.addEventListener("mousemove", (event) => {

    if (!neuralVisual) {
        return;
    }

    const x = (event.clientX / window.innerWidth - 0.5) * 15;
    const y = (event.clientY / window.innerHeight - 0.5) * 15;

    neuralVisual.style.transform =
        `translate(${x}px, ${y}px)`;

});


/* ============================= */
/* NAVBAR SCROLL */
/* ============================= */

const navbar = document.querySelector(".navbar");

window.addEventListener("scroll", () => {

    if (window.scrollY > 50) {

        navbar.style.background =
            "rgba(5,5,8,0.85)";

        navbar.style.backdropFilter =
            "blur(15px)";

    } else {

        navbar.style.background =
            "transparent";

        navbar.style.backdropFilter =
            "none";

    }

});