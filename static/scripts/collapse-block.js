function toggleTheory() {
    const block = document.getElementById("theory-block");
    const icon = document.querySelector(".theory-toggle i");

    block.classList.toggle("show");

    if (block.classList.contains("show")) {
        icon.classList.remove("fa-chevron-down");
        icon.classList.add("fa-chevron-up");
    } else {
        icon.classList.remove("fa-chevron-up");
        icon.classList.add("fa-chevron-down");
    }
}