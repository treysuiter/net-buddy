const loadingMessage = document.querySelector(".loading-message")
console.log("javascript working")

document.querySelector(".router-create-form").addEventListener("submit", () => {
    console.log("this ran")
    loadingMessage.show()
    }
)