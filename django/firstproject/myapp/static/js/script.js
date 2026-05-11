// EXPLORE BUTTON

document.getElementById("exploreBtn").addEventListener("click", () => {

    window.scrollTo({
        top: window.innerHeight,
        behavior: "smooth"
    });

});


// COUNTER ANIMATION

const counters = document.querySelectorAll(".counter");

counters.forEach(counter => {

    const updateCounter = () => {

        const target = +counter.getAttribute("data-target");
        const current = +counter.innerText;

        const increment = target / 100;

        if(current < target){

            counter.innerText = Math.ceil(current + increment);

            setTimeout(updateCounter, 20);

        }else{

            counter.innerText = target;
        }
    };

    updateCounter();
});


// DJANGO FACTS

const facts = [

    "Django was created to help developers build applications quickly.",

    "Instagram uses Django for handling millions of users.",

    "Django follows the DRY principle: Don't Repeat Yourself.",

    "Django includes a powerful admin panel out of the box.",

    "Django ORM lets you work with databases using Python."
];

const factBox = document.getElementById("factBox");

document.getElementById("factBtn").addEventListener("click", () => {

    const randomFact = facts[Math.floor(Math.random() * facts.length)];

    factBox.style.transform = "scale(0.9)";

    setTimeout(() => {

        factBox.innerText = randomFact;

        factBox.style.transform = "scale(1)";

    }, 200);

});