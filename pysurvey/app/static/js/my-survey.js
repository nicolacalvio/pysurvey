
var xhttp1 = new XMLHttpRequest();
xhttp1.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       if(xhttp1.responseText == "1"){
           document.getElementById("crea_sondaggio").classList.remove("hidden");
       }
    }
};
xhttp1.open("GET", "/logged", true);
xhttp1.send();


var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
        let div = document.getElementById("contenitore");
        try {
            let json = JSON.parse(xhttp.responseText).json_list;
            json.forEach((elemento)=>{
                /*
                <div class="flex py-3 px-4 rounded-lg text-gray-500 font-semibold cursor-pointer">
                    <span>All categorie</span>
                </div>
                <div class="bg-red-600 py-3 px-5 text-white font-semibold rounded-lg hover:shadow-lg transition duration-3000 cursor-pointer">
                    <span>Vai al sondaggio</span>
                </div>
                 */
                let divGrande = document.createElement("div");
                divGrande.classList.add("flex","w-8/12", "m-4", "p-6", "bg-white", "rounded-xl", "shadow-lg", "hover:shadow-xl", "transform", "hover:scale-105", "transition", "duration-500");

                let nuovo = document.createElement("div");
                //nuovo.innerText = elemento.titolo;
                nuovo.classList.add("flex", "flex-1","w-4/5","py-3", "px-4", "rounded-lg", "text-gray-500", "font-semibold");
                nuovo.id = elemento.idSurvey;
                let spanTitolo = document.createElement("span");
                spanTitolo.classList.add("px-5", "text-xl");
                spanTitolo.innerText = elemento.titolo;
                nuovo.appendChild(spanTitolo);
                divGrande.appendChild(nuovo);

                let nuovoBottone = document.createElement("div");
                nuovoBottone.classList.add("flex", "bg-red-600", "py-3", "px-5", "text-white", "font-semibold", "rounded-lg", "hover:shadow-lg", "transition", "duration-3000", "cursor-pointer");
                let spanBottone = document.createElement("span");
                spanBottone.innerText = "Vai!!";
                nuovoBottone.appendChild(spanBottone);
                //bottone riusultati
                let risBottone = document.createElement("div");
                risBottone.classList.add("flex", "bg-green-100", "py-3", "px-5", "mx-2", "font-semibold", "rounded-lg", "hover:shadow-lg", "transition", "duration-3000", "cursor-pointer");
                let spanRis = document.createElement("span");
                spanRis.innerText = "Risultati";
                risBottone.appendChild(spanRis);

                divGrande.appendChild(risBottone);
                divGrande.appendChild(nuovoBottone);

                nuovoBottone.addEventListener("click", ()=>{
                    window.location.href = "/survey?id="+elemento.idSurvey;
                })

                risBottone.addEventListener("click", ()=>{
                    window.location.href = "/statistiche?id="+elemento.idSurvey;
                })

                div.appendChild(divGrande);
            })


        } catch (e) {
            let nuovo = document.createElement("div");
            nuovo.innerText = xhttp.responseText;
            div.appendChild(nuovo);
        }
    }
};
xhttp.open("GET", "/titoloEId", true);
xhttp.send();