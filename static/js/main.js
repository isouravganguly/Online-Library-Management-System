/*=============== SHOW MENU ===============*/
const navMenu = document.getElementById('nav-menu'),
      navToggle = document.getElementById('nav-toggle'),
      navClose = document.getElementById('nav-close')

// =============== SCROLL OVERLAY ==============================
// navMenu.scrollableOverlay()


/*===== MENU SHOW =====*/
/* Validate if constant exists */
if(navToggle){
    navToggle.addEventListener('click', () =>{
        navMenu.classList.add('show-menu')
    })
}

/*===== MENU HIDDEN =====*/
/* Validate if constant exists */
if(navClose){
    navClose.addEventListener('click', () =>{
        navMenu.classList.remove('show-menu')
    })
}

/*=============== REMOVE MENU MOBILE ===============*/
const navLink = document.querySelectorAll('.nav__link')

function linkAction(){
    const navMenu = document.getElementById('nav-menu')
    // When we click on each nav__link, we remove the show-menu class
    navMenu.classList.remove('show-menu')
}
navLink.forEach(n => n.addEventListener('click', linkAction))

/*=============== CHANGE BACKGROUND HEADER ===============*/
function scrollHeader(){
    const header = document.getElementById('header')
    // When the scroll is greater than 80 viewport height, add the scroll-header class to the header tag
    if(this.scrollY >= 80) header.classList.add('scroll-header'); else header.classList.remove('scroll-header')
}
window.addEventListener('scroll', scrollHeader)


// ==============================  TUTORIAL WINDOW START SCREEN  =====================================
const modalViews = document.querySelectorAll('.tutorial__modal'),
    modalBtns = document.querySelectorAll('.tutorial__modal-next')
   var up = document.getElementById('nav-toggle-icon')
    // modalCloses= document.querySelectorAll('.project__modal-close')

let modal = function(modalClick){
    modalViews[modalClick].classList.remove('active-modal')
    modalViews[modalClick+1].classList.add('active-modal')

    if(modalClick==0){
    up.classList.add('upper')
    }

    if(modalClick==1){
        navMenu.classList.add('show-menu')
        up.classList.remove('upper')
        up = document.getElementById('book-list')
        up.classList.add('upper')
        }
    
    if(modalClick==2){
        up.classList.remove('upper')
        up = document.getElementById('log-in')
        up.classList.add('upper')
        }
    
    if(modalClick==3){
        navMenu.classList.remove('show-menu')
        up.classList.remove('upper')
            }
    
}

modalBtns.forEach((modalBtn,i) => {
    modalBtn.addEventListener('click', () => {
        modal(i)
        console.log(i)
    })
})


/*=============== DARK LIGHT THEME ===============*/ 
const themeButton = document.getElementById('theme-button')
const darkTheme = 'dark-theme'
const iconTheme = 'ri-sun-line'

// Previously selected topic (if user selected)
const selectedTheme = localStorage.getItem('selected-theme')
const selectedIcon = localStorage.getItem('selected-icon')

// We obtain the current theme that the interface has by validating the dark-theme class
const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light'
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'ri-moon-line' : 'ri-sun-line'

// We validate if the user previously chose a topic
if (selectedTheme) {
  // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the dark
  document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme)
  themeButton.classList[selectedIcon === 'ri-moon-line' ? 'add' : 'remove'](iconTheme)
}

// Activate / deactivate the theme manually with the button
themeButton.addEventListener('click', () => {
    // Add or remove the dark / icon theme
    document.body.classList.toggle(darkTheme)
    themeButton.classList.toggle(iconTheme)
    // We save the theme and the current icon that the user chose
    localStorage.setItem('selected-theme', getCurrentTheme())
    localStorage.setItem('selected-icon', getCurrentIcon())
})
