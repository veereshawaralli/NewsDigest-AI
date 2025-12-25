function countWords() {
    let text = document.getElementById("article").value.trim();
    let count = text === "" ? 0 : text.split(/\s+/).length;
    document.getElementById("wordCount").innerText = count + " words";
}

function showLoader() {
    document.getElementById("loader").classList.remove("hidden");
}
