/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
      navToggle = document.getElementById('nav-toggle'),
      navClose = document.getElementById('nav-close')

/* Menu show */
if (navToggle) {
    navToggle.addEventListener('click', () =>{
       navMenu.classList.add('show-menu')
    })
}

/* Menu hidden */
if (navClose) {
    navClose.addEventListener('click', () =>{
       navMenu.classList.remove('show-menu')
    })
}

/*=============== SEARCH ===============*/
const search = document.getElementById('search'),
      searchBtn = document.getElementById('search-btn'),
      searchClose = document.getElementById('search-close')

/* Search show */
if (searchBtn && search) {
    searchBtn.addEventListener('click', () =>{
       search.classList.add('show-search')
    })
}

/* Search hidden */
if (searchClose && search) {
    searchClose.addEventListener('click', () =>{
       search.classList.remove('show-search')
    })
}

/*=============== LOGIN ===============*/
const login = document.getElementById('login'),
      loginBtn = document.getElementById('login-btn'),
      loginClose = document.getElementById('login-close')

/* Login show */
if (loginBtn && login) {
    loginBtn.addEventListener('click', () =>{
       login.classList.add('show-login')
    })
}

/* Login hidden */
if (loginClose && login) {
    loginClose.addEventListener('click', () =>{
       login.classList.remove('show-login')
    })
}
