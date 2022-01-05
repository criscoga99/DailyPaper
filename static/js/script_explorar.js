cont = 1;
function mostrarFiltros(){
    cont++;
    if (cont%2==0){
        document.getElementById("filtros").style.display="block";
    }
    else {
        document.getElementById("filtros").style.display="none";
    }
    
}