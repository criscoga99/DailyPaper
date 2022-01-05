cont_redactar = 1;
cont_usuario = 1;
cont_publicaciones = 1;
cont_filtros = 1;
function mostrarRedaccion(){
    cont_redactar ++;
    if (cont_redactar%2==0) {
        document.getElementById("redactar").style.display="block";

    }
    else {
        document.getElementById("redactar").style.display="none";
    }
}
function confirmarBorradoUsuario() {
    alert("Usuario eliminado");
}
function confirmarBorradoPublicacion() {
    alert("Publicación eliminada");
}
function mostrarTablaUsuarios(){
    cont_usuario ++;
    if (cont_usuario%2==0) {
        document.getElementById("usuarios").style.display="block";

    }
    else {
        document.getElementById("usuarios").style.display="none";
    }
}
function mostrarTablaPublicaciones(){
    cont_publicaciones ++;
    if (cont_publicaciones%2==0) {
        document.getElementById("publicaciones").style.display="block";

    }
    else {
        document.getElementById("publicaciones").style.display="none";
    }
}
function mostrarFiltrosUsuarios(){
    cont_filtros ++;
    if (cont_filtros%2==0) {
        document.getElementById("filtrosUsuarios").style.display="block";

    }
    else {
        document.getElementById("filtrosUsuarios").style.display="none";
    }
}