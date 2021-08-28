/*
setInterval(()=>{
    if(document.getElementsByClassName("domande").length == contaChecked()){
        document.getElementById("salva").classList.remove("cursor-not-allowed");
        document.getElementById("salva").addEventListener("click", salva);
    }else{
        document.getElementById("salva").classList.add("cursor-not-allowed");
        document.getElementById("salva").removeEventListener("click", salva);
    }
}, 100)
 */
document.getElementById("salva").addEventListener("click", salva);

    function salva(){
        //prende tutte le radio checked, il loro id e lo serializza
        let risposteCheckate = [];
        let i=0;
        document.querySelectorAll(".risposta").forEach((elemento)=>{
            if(elemento.checked){
                let indici = elemento.id.split('_');
                risposteCheckate[i] = Object.create(null)
                risposteCheckate[i]["idDomanda"] = String(indici[0]);
                risposteCheckate[i]["idRisposta"] = String(indici[1]);
                i++;
            }
        })
        console.log(risposteCheckate);
        //mando il json al backend
        var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
        var theUrl = "/inviaRisposta";
        xmlhttp.open("POST", theUrl);
        xmlhttp.setRequestHeader("Content-Type", "application/json");
        xmlhttp.send(JSON.stringify(risposteCheckate));
        alert("inviato con successo");
        window.location.href="/my-survey";
    }

    function colora(id){
        //id=iddomanda_idrisposta
        //coloro l'attuale se non è colorata
        //se una della stessa domanda è colorata allora la decoloro e coloro questa
        let questo = document.getElementById(id);
        if(questo.checked){
            questo.parentNode.style.backgroundColor = "#E5E7EB";
        }
        let vicini = document.getElementsByName(String(id.split('_')[0]));
        vicini.forEach((elem)=>{
            if(!elem.checked){
                if(elem.parentNode.style.backgroundColor == "rgb(229, 231, 235)"){
                    elem.parentNode.style.backgroundColor = '';
                }
            }
        })
}

function contaChecked(){
        const risposte = document.querySelectorAll(".risposta");
        let cont=0;
        risposte.forEach((elem)=>{
            if(elem.checked){
                cont++;
            }
        })
        return cont;
}