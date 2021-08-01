controllaAccesso();
controllaAccessoMobile();
//uso i cookie invece che condizioni con le sessioni lato backend per togliere carico al backend
//pianifico la struttura della mia applicazione in modo da sostenere elevati carichi
//N.B non usare i cookie per prendere i dati in quanto l'utente può modificarli, usare sempre la sessione
function controllaAccesso(){
    const changeUI  = () =>{
        var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                   if(xhttp.responseText == "1"){
                       document.getElementById("non_loggato").style.display = 'none'; //levo singup e signin
                       document.getElementById("immagine_profilo").style.display = 'block'; //mostro img_profilo
                   }
                }
            };
            xhttp.open("GET", "/logged", true);
            xhttp.send();
    }
    changeUI();
}

function controllaAccessoMobile(){
    const changeLinks = () =>{
        var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                   let profilo_mobile = document.getElementById('profilo_mobile');
                   profilo_mobile.href = (xhttp.responseText == "1") ? "/my-account" : "/login";
                }
            };
            xhttp.open("GET", "/logged", true);
            xhttp.send();
    }
    changeLinks();
}