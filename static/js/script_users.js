cont_redactar = 1;
function mostrarRedaccion(){
    cont_redactar ++;
    if (cont_redactar%2==0) {
        document.getElementById("redactar").style.display="block";

    }
    else {
        document.getElementById("redactar").style.display="none";
    }
}