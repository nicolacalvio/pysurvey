controllaAccesso();
controllaAccessoMobile();
//uso i cookie invece che condizioni con le sessioni lato backend per togliere carico al backend
//pianifico la struttura della mia applicazione in modo da sostenere elevati carichi
//N.B non usare i cookie per prendere i dati in quanto l'utente può modificarli, usare sempre la sessione
function controllaAccesso(){
    const getCookie = (cookie_name) =>{
         const re = new RegExp(`(?<=${cookie_name}=)[^;]*`);
         try{
              return document.cookie.match(re)[0];	// Will raise TypeError if cookie is not found
         }catch{
              return undefined;
         }
    }
    const changeUI  = () =>{
        let idUser = getCookie('loggato');
        if(idUser !== undefined){
            //utente loggato
            document.getElementById("non_loggato").style.display = 'none'; //levo singup e signin
            document.getElementById("immagine_profilo").style.display = 'block'; //mostro img_profilo
        }
    }
    changeUI();
}

function controllaAccessoMobile(){
    const getCookie = (cookie_name) =>{
         const re = new RegExp(`(?<=${cookie_name}=)[^;]*`);
         try{
              return document.cookie.match(re)[0];	// Will raise TypeError if cookie is not found
         }catch{
              return undefined;
         }
    }
    const changeLinks = () =>{
        let idUser = getCookie('loggato');
        let profilo_mobile = document.getElementById('profilo_mobile');
        profilo_mobile.href = (idUser !== undefined) ? "/my-account" : "/login";
    }
    changeLinks();
}