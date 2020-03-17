// const loadingMessage = document.querySelector(".loading-message")

// document.querySelectorAll(".router-create-form").addEventListener("submit", () => {
//     loadingMessage.show()
//     }
// )

document.querySelector(".router-create-form").addEventListener("submit", (evt) => {
    if (evt.target.id.startsWith("show")) {
        infoDialog.show()
    }
})

// const loadingMessage = document.querySelector(".loading-message")

// document.querySelectorAll(".router-create-form").addEventListener("submit", () => {
//     loadingMessage.show()
//     }
// )