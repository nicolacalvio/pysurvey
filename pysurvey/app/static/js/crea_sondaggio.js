var n_domande_value=1;
        //clono la prima domanda prima di qualunque cosa (ci servirà per aggiungere la domanda)
        let cloneDomanda=document.querySelectorAll(".domandina")[0].cloneNode(true);

        let idSurvey =-1;
        //per aggiungere le risposte
        let risposte=document.querySelectorAll(".risposta")[0];
        risposte.addEventListener('keypress', enter_premuto);

        function enter_premuto(tasto){
            if (tasto.key === "Enter"){
                let nuovaRisp= risposte.cloneNode(true);
                risposte.parentNode.appendChild(nuovaRisp);
                nuovaRisp.addEventListener("keypress", enter_premuto)
                nuovaRisp.value = "";
                nuovaRisp.focus()
            }
        }



        //per aggiungere la domanda
         //0.aggiungo eventlisener al div tratteggiato
        //1.clono il div tratteggiato
         //1.5 mi salvo il riferiemnto del padre del div tratteggiato
        //2. rimuovo il div trattegiato
        //3.clono il clone della domanda
        //4. aggiungo al padre del div tratteggiato il nuovo clone


        let tratteggiato=document.querySelectorAll(".domandaTrattegiata")[0];
        let parentTratteggiato = tratteggiato.parentNode;
        tratteggiato.addEventListener("click", aggiungiDomanda)
        document.getElementById("salva").addEventListener("click", salvaSurvey);

        function aggiungiDomanda(){
            let cloneCloneDomanda=cloneDomanda.cloneNode(true);
            let pulsante_salva = document.getElementById("salva");
            let clone_pulsante_salva = pulsante_salva.cloneNode(true);
            cloneCloneDomanda.querySelectorAll(".radiobutton").forEach((elemento)=>{
                elemento.name = "n_domande"+n_domande_value;
            })
            cloneCloneDomanda.querySelectorAll(".domanda")[0].name="domanda"+n_domande_value;
            cloneCloneDomanda.querySelectorAll(".risposta")[0].name = "risposta"+n_domande_value;
            n_domande_value++;
            let risposteCloneCloneDomanda = cloneCloneDomanda.querySelectorAll(".risposta")[0];
            risposteCloneCloneDomanda.addEventListener('keypress', premutoBottone)
            parentTratteggiato.appendChild(cloneCloneDomanda);
            let cloneClonatoTrattegiato = tratteggiato.cloneNode(true);
            cloneClonatoTrattegiato.addEventListener("click", aggiungiDomanda);
            parentTratteggiato.appendChild(cloneClonatoTrattegiato);
            pulsante_salva.remove();
            parentTratteggiato.appendChild(clone_pulsante_salva);
            clone_pulsante_salva.addEventListener("click", salvaSurvey);
            function premutoBottone(tasto){
                    if (tasto.key === "Enter"){
                    let nuovaRisp= risposteCloneCloneDomanda.cloneNode(true);
                    risposteCloneCloneDomanda.parentNode.appendChild(nuovaRisp);
                    nuovaRisp.addEventListener("keypress", premutoBottone)
                    nuovaRisp.value = "";
                    nuovaRisp.focus()
                }
            }
            this.remove();

        }

        function copyToClipboard() {
           while(idSurvey === -1){} //busy waiting della richiesta async
           let text = window.location.href.replace("crea", "survey?id="+idSurvey);
           const elem = document.createElement('textarea');
           elem.value = text;
           document.body.appendChild(elem);
           elem.select();
           document.execCommand('copy');
           document.body.removeChild(elem);
           document.getElementById("copiaUrl").innerText = "Copiato!";
           document.getElementById("icona").src="/static/img/smile.png"
        }

        function salvaSurvey(){
            //TODO: mandare tutte le domande e le risposte al backend che creerà la survey
            //l'id dello user lo ha già il backend tramite il cookie di sessione
            //le domande sono contrassegnate da name -> domanda+index
            //le risposte di una data domanda sono contrassegnate da name -> risposta+index_domanda
            //le radio button sono contrassegnate da name -> n_domande+index_domanda
            if(document.getElementById("titolo").value !== ""){
                let oggettone = Object.create(null);
                oggettone.titolo = document.getElementById("titolo").value;
                oggettone[0] = Object.create(null);
                for(let i=0; document.getElementsByName("domanda"+i).length!==0; i++){
                    oggettone[i].domande = document.getElementsByName("domanda"+i)[0].value;
                    oggettone[i].risposte = Object.create(null);
                    let j=0;
                    document.getElementsByName("risposta"+i).forEach((elemento) =>{
                        oggettone[i]["risposte"][j]=elemento.value;
                        j++;
                    })

                    let tipoDomanda;
                    document.getElementsByName("n_domande" + i).forEach((elemento)=>{
                        if(elemento.checked){
                            tipoDomanda =elemento.value === "una";
                        }
                    });

                    oggettone[i].selezione = tipoDomanda;
                    oggettone[i+1] = Object.create(null);
                }
                //console.log(JSON.stringify(oggettone));
                var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
                var theUrl = "/creaSurvey";
                xmlhttp.open("POST", theUrl);
                xmlhttp.setRequestHeader("Content-Type", "application/json");
                xmlhttp.send(JSON.stringify(oggettone));
                xmlhttp.onreadystatechange = function() { // Call a function when the state changes.
                    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                        idSurvey = xmlhttp.responseText;
                    }
                }
                document.getElementById("mega_contenitore").classList.remove("hidden");
                //window.location.href = "/my-survey";
            }else{
                alert("devi impostare un titolo alla survey!");
            }

        }

