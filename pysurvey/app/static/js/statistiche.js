//chiamata Ajax
var torte = [];
var index=-1;

const queryString = window.location.search;
const parameters = new URLSearchParams(queryString);
const id = parameters.get('id');

const bigParent = document.getElementById("contenitore");

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       const oggettone = JSON.parse(xhttp.responseText);
       console.log(oggettone);
       let domandaPrev = oggettone["json_list"][0].idDomanda;
       for (let elemento in oggettone["json_list"]){
           console.log(oggettone["json_list"][elemento]);
           if(oggettone["json_list"][elemento].idDomanda === domandaPrev && elemento!=0){
               //aggiungo la risposta al grafico a torta
               torte[index].data.labels.push(oggettone["json_list"][elemento].risposta)
               torte[index].data.datasets.forEach((dataset) => {
                    dataset.data.push(oggettone["json_list"][elemento].numeroRisposte);
                });
               const r = () => Math.random() * 256 >> 0;
               torte[index].data.datasets.forEach((dataset) => {
                    dataset.backgroundColor.push(`rgb(${r()}, ${r()}, ${r()})`);
                });
               //torta.datasets.backgroundColor = `rgb(${r()}, ${r()}, ${r()})`
               torte[index].update();
           }else{
               //aggiungo la domanda alla pagina e a fianco ci metto il grafico a torta con la prima risposta

               let h4 = document.createElement('h2');
               h4.classList.add("text-2xl", "font-semibold", "text-gray-500", "dark:text-light")
               h4.innerText = oggettone["json_list"][elemento].domanda;

               let primoDiv = document.createElement('div');
               primoDiv.classList.add("flex", "items-center");

               let secondoDiv = document.createElement('div');
               secondoDiv.classList.add("relative", "p-4");

               let canvas = document.createElement('canvas');
               canvas.id = oggettone["json_list"][elemento].idDomanda;
               canvas.width=350;
               canvas.height=350;
               secondoDiv.appendChild(canvas);
               primoDiv.appendChild(secondoDiv);
               h4.appendChild(primoDiv);
               bigParent.appendChild(h4);

               //creo grafico
               const grafico = document.getElementById(oggettone["json_list"][elemento].idDomanda);
               const torta = new Chart(grafico, {
                type: 'doughnut',
                data: {
                    labels: [
              ],
              datasets: [{
                label: oggettone["json_list"][elemento].domanda,
                data: [],
                backgroundColor: [

                ],
                hoverOffset: 4
              }]
                },
                options: {
                            responsive: false
                        }
            });
               console.log(torta);
               torta.data.labels.push(oggettone["json_list"][elemento].risposta);
               torta.data.datasets.forEach((dataset) => {
                    dataset.data.push(oggettone["json_list"][elemento].numeroRisposte);
                });
               const r = () => Math.random() * 256 >> 0;
               torta.data.datasets.forEach((dataset) => {
                    dataset.backgroundColor.push(`rgb(${r()}, ${r()}, ${r()})`);
                });
               //torta.datasets.backgroundColor = `rgb(${r()}, ${r()}, ${r()})`
               torta.update();
               torte.push(torta);
               index++;
               domandaPrev = oggettone["json_list"][elemento].idDomanda;
           }
       }
    }
};
xhttp.open("GET", "/ritorna-risultati?id="+id, true);
xhttp.send();

/*
var ctx = document.getElementById('myChart');
var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: [
    'Red',
    'Blue',
    'Yellow'
  ],
  datasets: [{
    label: 'My First Dataset',
    data: [300, 50, 100],
    backgroundColor: [
      'rgb(255, 99, 132)',
      'rgb(54, 162, 235)',
      'rgb(255, 205, 86)'
    ],
    hoverOffset: 4
  }]
    },
    options: {
                responsive: false
            }
});
 */