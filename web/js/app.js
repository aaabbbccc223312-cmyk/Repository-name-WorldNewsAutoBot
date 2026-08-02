const tg = window.Telegram.WebApp;

tg.ready();

tg.expand();

const app = document.querySelector(".app");

const newsContainer = document.getElementById("news");

const categories = document.querySelectorAll(".categories button");

categories.forEach(button => {

    button.addEventListener("click", () => {

        categories.forEach(btn => {

            btn.style.background = "#2563eb";

        });

        button.style.background = "#0ea5e9";

    });

});

async function loadNews() {

    try {

        const response = await fetch("/api/news");

        if (!response.ok) {

            throw new Error("Unable to load news");

        }

        const articles = await response.json();

        newsContainer.innerHTML = "";

        articles.forEach(article => {

            newsContainer.innerHTML += `

                <div class="card">

                    <img src="${article.image}" alt="News">

                    <h2>${article.title}</h2>

                    <p>${article.summary}</p>

                    <button onclick="window.open('${article.url}','_blank')">

                        Read More

                    </button>

                </div>

            `;

        });

    }

    catch (error) {

        console.log(error);

    }

}

loadNews();

setInterval(

    loadNews,

    60000

);
