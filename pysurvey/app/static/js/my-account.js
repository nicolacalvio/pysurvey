document.getElementById("modifica").addEventListener("click", modificaSchermata);
            function salva() {
                const campi = [document.querySelectorAll("#username")[0], document.querySelectorAll("#mail")[0], document.querySelectorAll("#nazionalita")[0]];
                const classi = [campi[0].classList, campi[1].classList];
                const placeholders = [document.getElementById("userplaceholder"), document.getElementById("mailplaceholder"), document.getElementById("nazionalitaplaceholder")];
                const nuovo_placeHolder = [document.createElement("div"), document.createElement("div")];
                /*
                nuovo_placeHolder[0].id = "userplaceholder";
                nuovo_placeHolder[0].innerText = "username";
                nuovo_placeHolder[1].id = "mailplaceholder";
                nuovo_placeHolder[1].innerText = "mail";
                */
                //cambio gli input con gli h1 di prima
                campi.forEach((elemento, indice)=>{
                    if(elemento){
                    if(indice!==2){
                       const testo = elemento.value;
                       const genitore = elemento.parentNode;
                       const idElemento = elemento.id;
                       elemento.remove();
                       //placeholders[indice].remove();
                       const nuovo = document.createElement("div");
                       nuovo.innerText = testo;
                       nuovo.classList=classi[indice];
                       nuovo.id = idElemento;
                       genitore.appendChild(nuovo);
                       genitore.appendChild(nuovo_placeHolder[indice]);
                    }else{
                        const boxmodificanazionalita = document.getElementById("boxmodificanazionalita");
                        const boxnazionalita = document.getElementById("boxnazionalita");
                        document.getElementById('nazionalita').innerText=document.getElementById('country').value;
                        boxmodificanazionalita.classList.add("hidden");
                        boxnazionalita.classList.remove("hidden");

                    }

                }
                });
                //chiamata a API per salvare i nuovi dati inseriti
                const nome=document.querySelectorAll("#username")[0].innerText, mail=document.querySelectorAll("#mail")[0].innerText,
                    nazionalita=document.querySelectorAll("#nazionalita")[0].innerText;
                document.getElementById("nome_utente").innerText = nome+"!";
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                       // Typical action to be performed when the document is ready:
                       console.log(xhttp.responseText);
                    }
                };
                xhttp.open("GET", "/modificaAccount?nome="+nome+"&mail="+mail+"&nazionalita="+nazionalita, true);
                xhttp.send();
                //cambio il bottone in modifica
                const modifica = document.getElementById("modifica");
                modifica.innerText = "modifica";
                modifica.removeEventListener("click", salva);
                modifica.addEventListener("click", modificaSchermata);
            }

            function modificaSchermata(){
            //trasformo mail e username
            console.log("cliccato");
            const campi = [document.querySelectorAll("#username")[0], document.querySelectorAll("#mail")[0], document.querySelectorAll("#nazionalita")[0]];
            const classi = [campi[0].classList, campi[1].classList];
            /*
            const placeholders = [document.getElementById("userplaceholder"), document.getElementById("mailplaceholder"), document.getElementById("nazionalitaplaceholder")];
            const nuovo_placeHolder = [document.createElement("div"), document.createElement("div")];
            nuovo_placeHolder[0].id = "userplaceholder";
            nuovo_placeHolder[0].innerText = "username";
            nuovo_placeHolder[1].id = "mailplaceholder";
            nuovo_placeHolder[1].innerText = "mail";

             */
            for(let i=0; i<document.getElementById("country").options.length;i++){
                            if(document.getElementById("country").options[i].innerText===document.getElementById('nazionalita').innerText) {
                                document.getElementById("country").selectedIndex = i;
                                break;
                            }
                        }
            /*
            nuovo_placeHolder[2].id = "nazionalitaplaceholder";
            nuovo_placeHolder[2].innerText = "nazionalità";
            */

            campi.forEach((elemento, indice)=>{
                if(elemento){
                    if(indice!==2){
                       const testo = elemento.innerText;
                       const genitore = elemento.parentNode;
                       const idElemento = elemento.id;
                       elemento.remove();
                       //placeholders[indice].remove();
                       const nuovo = document.createElement("input");
                       nuovo.type = "text";
                       nuovo.value = testo;
                       nuovo.classList=classi[indice];
                       nuovo.id = idElemento;
                       genitore.appendChild(nuovo);
                       //genitore.appendChild(nuovo_placeHolder[indice]);
                    }else{
                        const boxnazionalita = document.getElementById("boxnazionalita");
                        boxnazionalita.classList.add("hidden");
                        const boxmodificanazionalita = document.getElementById("boxmodificanazionalita");
                        boxmodificanazionalita.classList.remove("hidden");
                        for(let i=0; i<document.getElementById("country").options.length;i++){
                            if(document.getElementById("country").options[i].innerText===document.getElementById('nazionalita').innerText) {
                                document.getElementById("country").selectedIndex = i;
                                break;
                            }
                        }
                    }

                }
            });
            //dentro l'immagine ci metto un bottone cambia
            //il tasto modifica diventa salva
            const modifica = document.getElementById("modifica");
            modifica.innerText = "salva";
            modifica.removeEventListener("click", modificaSchermata);
            modifica.addEventListener("click", salva);
        }