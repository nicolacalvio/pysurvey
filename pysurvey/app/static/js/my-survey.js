
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
            let nuovo = "<div class=\"bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4\">\n" +
                "        <div class=\"sm:flex sm:items-start\">\n" +
                "          <div class=\"mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10\">\n" +
                "            <!-- Heroicon name: outline/exclamation -->\n" +
                "            <svg class=\"h-6 w-6 text-red-600\" xmlns=\"http://www.w3.org/2000/svg\" fill=\"none\" viewBox=\"0 0 24 24\" stroke=\"currentColor\" aria-hidden=\"true\">\n" +
                "              <path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z\" />\n" +
                "            </svg>\n" +
                "          </div>\n" +
                "          <div class=\"mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left\">\n" +
                "            <h3 class=\"text-lg leading-6 font-medium text-gray-900\" id=\"modal-title\">\n" +
                                 xhttp.responseText   +
                "            </h3>\n" +
                "          </div>\n" +
                "        </div>\n" +
                "      </div>";
            div.innerHTML = nuovo;
        }
    }
};
xhttp.open("GET", "/titoloEId", true);
xhttp.send();