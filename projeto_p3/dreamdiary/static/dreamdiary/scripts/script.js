window.addEventListener("scroll", function () {
    let navbar = document.getElementById("navbar");
    
    if (window.scrollY > 50) { // Quando o scroll passar de 50px
        navbar.classList.add("scrolled");
    } else {
        navbar.classList.remove("scrolled");
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const menuBtn = document.getElementById("menu-btn");
    const navbarMenu = document.getElementById("navbar-menu");
    const header = document.querySelector("navbar");

    // Alterna o menu quando clicar no botão hambúrguer
    menuBtn.addEventListener("click", function () {
        navbarMenu.classList.toggle("show");
    });
});

const btn_form = document.getElementById('btn-form')

btn_form.addEventListener('click', (e) => {
    e.defaultPrevented();
})