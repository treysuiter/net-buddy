const navLoadingMessage = document.querySelector(".navLoadingMessage")


document.querySelector(".navList").addEventListener("click", (evt) => {
    if (evt.target.id === "current-router-info-link") {
        navLoadingMessage.show()
    }
}
)

document.querySelector(".navList").addEventListener("click", (evt) => {
    if (evt.target.id === "home-link") {
        navLoadingMessage.show()
    }
}
)

document.querySelector(".router-form").addEventListener("submit", () => {
    navLoadingMessage.show()
    }
)