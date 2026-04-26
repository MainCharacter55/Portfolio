/* static/js/hobbies.js */
"use strict";

(function initHobbiesSnap() {
    const wrapper = document.querySelector(".hobbies-main-wrapper");

    if (!wrapper) {
        return;
    }

    const snapSections = document.querySelectorAll(".horizontal-snap");

    if (!snapSections.length) {
        return;
    }

    const centerHobby = (element) => {
        const firstSlide = element.querySelector(".hobby-slide");

        if (!firstSlide) {
            return;
        }

        element.scrollTo({
            left: firstSlide.offsetWidth,
            behavior: "auto",
        });
    };

    const recenterAll = () => {
        snapSections.forEach(centerHobby);
    };

    window.addEventListener("load", () => {
        setTimeout(recenterAll, 50);
    });

    window.addEventListener("resize", recenterAll);

    const hobbyObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    const firstSlide = entry.target.querySelector(".hobby-slide");
                    const centerOffset = firstSlide ? firstSlide.offsetWidth : window.innerWidth;

                    entry.target.scrollTo({
                        left: centerOffset,
                        behavior: "auto",
                    });
                }
            });
        },
        {
            threshold: 0.01,
            rootMargin: "-35% 0px -35% 0px",
        }
    );

    const shouldReset = (section) => {
        const rect = section.getBoundingClientRect();
        const upperBound = window.innerHeight * 0.15;
        const lowerBound = window.innerHeight * 0.85;

        return rect.bottom < upperBound || rect.top > lowerBound;
    };

    // Keep each horizontal section entering from a predictable centered state.
    const resetOffscreenSections = () => {
        snapSections.forEach((section) => {
            if (shouldReset(section)) {
                centerHobby(section);
            }
        });
    };

    window.addEventListener("scroll", resetOffscreenSections, { passive: true });

    snapSections.forEach((section) => {
        hobbyObserver.observe(section);
    });
})();
