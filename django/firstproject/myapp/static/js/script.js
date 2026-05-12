// Interactive Mouse Glow
document.addEventListener("mousemove", (e) => {

    const circles = document.querySelectorAll(".circle");

    circles.forEach((circle, index) => {

        const speed = (index + 1) * 0.02;

        const x = (window.innerWidth - e.pageX * speed) / 100;
        const y = (window.innerHeight - e.pageY * speed) / 100;

        circle.style.transform =
        `translate(${x}px, ${y}px)`;
    });
});

// Profile Button
const magicBtn = document.getElementById("magicBtn");

if(magicBtn){

    magicBtn.addEventListener("click", () => {

        const text = document.getElementById("powerText");

        text.innerHTML =
        "⚡ Django Power Activated! Ready to build scalable AI-powered web apps.";

        text.style.marginTop = "20px";
        text.style.color = "#00ffe0";
    });
}

// Typing Effect
const heading = document.querySelector(".hero-content h1");

if(heading){

    const text = heading.innerText;

    heading.innerText = "";

    let i = 0;

    function type(){

        if(i < text.length){

            heading.innerHTML += text.charAt(i);

            i++;

            setTimeout(type, 50);
        }
    }

    type();
}