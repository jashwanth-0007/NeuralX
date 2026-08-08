const filterButtons =
    document.querySelectorAll(".filter-button");

const problemCards =
    document.querySelectorAll(".problem-card");


filterButtons.forEach((button) => {

    button.addEventListener("click", () => {

        const selectedFilter =
            button.getAttribute("data-filter");


        filterButtons.forEach((btn) => {

            btn.classList.remove("active");

        });


        button.classList.add("active");


        problemCards.forEach((card) => {

            const domain =
                card.getAttribute("data-domain");


            if (
                selectedFilter === "all" ||
                domain === selectedFilter
            ) {

                card.style.display = "flex";

                setTimeout(() => {
                    card.style.opacity = "1";
                }, 50);

            } else {

                card.style.opacity = "0";

                setTimeout(() => {
                    card.style.display = "none";
                }, 200);

            }

        });

    });

});