function mostrarLogin(){
    document.getElementById("login").style.display="block";
    document.getElementById("portada").style.display="none";
    document.getElementById("error").style.display="none";
}
function mostrarPortada(){
    document.getElementById("portada").style.display="block";
    document.getElementById("login").style.display="none";
    document.getElementById("register").style.display="none";
}
function mostrarRegistro(){
    document.getElementById("register").style.display="block";
    document.getElementById("login").style.display="none";
}
function volverLogin(){
    document.getElementById("login").style.display="block";
    document.getElementById("register").style.display="none";
}
function iluminarComenzar(){
    document.getElementById("btnComenzar").style.backgroundColor="#1ECF19";
}
function apagarComenzar(){
    document.getElementById("btnComenzar").style.backgroundColor="orange";
}
function iluminarVolver(){
    document.getElementById("btnVolver").style.color="orange";
    document.getElementById("btnVolver").style.backgroundColor="royalblue";
}
function apagarVolver(){
    document.getElementById("btnVolver").style.color="white";
    document.getElementById("btnVolver").style.backgroundColor="orange";
}
function iluminarLogin(){
    document.getElementById("btnLogin").style.backgroundColor="#1ECF19";
}
function apagarLogin(){
    document.getElementById("btnLogin").style.backgroundColor="orange";
}
function iluminarRegistrar(){
    document.getElementById("btnRegistrar").style.backgroundColor="#1ECF19";
}
function apagarRegistrar(){
    document.getElementById("btnRegistrar").style.backgroundColor="orange";
}
