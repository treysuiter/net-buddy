const navLoadingMessage = document.querySelector(".navLoadingMessage")


document.querySelector(".navList").addEventListener("click", (evt) => {
    if (evt.target.id === "current-router-info-link") {
        navLoadingMessage.show()
    }
}
)