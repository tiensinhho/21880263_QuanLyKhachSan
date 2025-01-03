(()=>{
    // if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    //     document.documentElement.setAttribute('data-bs-theme', 'dark');
    // } else {
    //     document.documentElement.setAttribute('data-bs-theme', 'light');
    // }
    get = getCookie("theme");
    const htmlElement = document.documentElement;
    if (get == "dark") {
        htmlElement.setAttribute('data-bs-theme', 'dark');
        setCookie("theme", "dark", 1);
    } else if (get == "light") {
        htmlElement.setAttribute('data-bs-theme', 'light');
        setCookie("theme", "light", 1);
    } else {
        auto_theme()
    }
})();

function getCookie(name) { 
    let cookieArr = document.cookie.split(";"); 
    for(let i = 0; i < cookieArr.length; i++) { 
        let cookiePair = cookieArr[i].split("="); 
        if(name == cookiePair[0].trim()) { 
            return decodeURIComponent(cookiePair[1]); 
        } 
    } return null; 
}
function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function toggleTheme() {
    const htmlElement = document.documentElement;
    const currentTheme = htmlElement.getAttribute('data-bs-theme');
    if (currentTheme === 'light') {
        htmlElement.setAttribute('data-bs-theme', 'dark');
        setCookie("theme", "dark", 7);
    } else {
        htmlElement.setAttribute('data-bs-theme', 'light');
        setCookie("theme", "light", 7);
    }
}

function auto_theme() {
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.setAttribute('data-bs-theme', 'dark');
    } else {
        document.documentElement.setAttribute('data-bs-theme', 'light');
    }
    setCookie("theme", "auto", 7);
}
