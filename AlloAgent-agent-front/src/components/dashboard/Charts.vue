<template>
    <v-container>
        <v-row>
            <v-col lg="6" cols="12" class="mx-auto">
                <v-card>
                    <div class="pa-5">
                        <h2>Ponderación por CATEGORÍA</h2>
                    </div>
                    <canvas id="myChart" width="100" height="20"></canvas>
                </v-card>
            </v-col>

            <v-col lg="6" cols="12" class="mx-auto">
                <v-card>
                    <div class="pa-5">
                        <h2>Ponderación de subcategorías por SALUDO Y PRESENTACIÓN</h2>
                    </div>
                    <canvas id="myChart1" width="100" height="20"></canvas>
                </v-card>
            </v-col>

            <v-col lg="6" cols="12" class="mx-auto">
                <v-card>
                    <div class="pa-5">
                        <h2>Ponderación de subcategorías por OBJETIVO LLAMADA</h2>
                    </div>
                    <canvas id="myChart2" width="100" height="20"></canvas>
                </v-card>
            </v-col>

            <v-col lg="6" cols="12" class="mx-auto">
                <v-card>
                    <div class="pa-5">
                        <h2>Ponderación de subcategorías por CIERRE Y DESPEDIDA</h2>
                    </div>
                    <canvas id="myChart3" width="100" height="20"></canvas>
                </v-card>
            </v-col>

            <v-col lg="12" cols="12" class="mx-auto">
                <v-card>
                    <div class="pa-5">
                        <h2>Cantidad de llamadas por TIPO DE LLAMADA</h2>
                    </div>
                    <canvas class="pa-5" id="myChart4" width="100" height="40"></canvas>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import {Vue, Component} from 'vue-property-decorator';
import Chart from 'chart.js/auto';
import axios from 'axios';

@Component({
    name: 'Charts'
})

export default class Charts extends Vue{

    public labels = [];
    public data = [];
    public labelcategoria = "";
    public labelTipoLlamada = "";

    mounted(): void {
        this.getChartGlobal();
        this.getChart('1');
        this.getChart('2');
        this.getChart('3');    
        this.getChartTipoLlamada();
    } 

    private getChartGlobal(){

        let headersList = {
            "Accept": "*/*",
            "Content-Type":"application/json",
            "Authorization": 'Basic ' + btoa('usuario1' + ':' + 'usuario1'),
            "Access-Control-Allow-Origin": "http://localhost:9000",
        }

        let config = {
            url: "http://127.0.0.1:9090/cardsget",
            method: "GET",
            headers: headersList,
            data: {}
        }
        
        axios(config)
        .then((response) => {
            let datos = response.data;
            for (let item of datos){
                let itemid = Object.values(item._id);	
                this.labels.push(itemid[1]);
                this.data.push(+item.Promedio)                     
            }

            const data = {
                labels: this.labels,
                datasets: [{
                    label: 'Ponderación de Categorías',
                    data: this.data,
                    fill: true,
                    backgroundColor: 'rgba(230,230,230,0.5)',
                    borderColor: 'rgb(112,179,178)',
                    pointBackgroundColor: 'rgb(112,179,178)',
                    pointBorderColor: '#7BB7AF',
                    pointHoverBackgroundColor: '#E4E4E4',
                    pointHoverBorderColor: 'rgb(126,185,182)'
                }]
            };
            const ctx = document.getElementById('myChart');
            const myChart = new Chart(ctx, {
                type: 'radar',
                data: data,
                options: {
                    elements: {
                        line: {
                            borderWidth: 3
                        }
                    },
                    plugins:{
                        legend:{
                            display: false
                        }
                    }
                },
            });
        })
        .finally(() => {
            this.labels = [];
            this.data = [];
        });       
    }

    private getChart(id_cat: string){

        let headersList = {
            "Accept": "*/*",
            "Content-Type":"application/json",
            "Authorization": 'Basic ' + btoa('usuario1' + ':' + 'usuario1'),
            "Access-Control-Allow-Origin": "http://localhost:9000",
        }

        let config = {
            url: "http://127.0.0.1:9090/chartget?id_cat=" + id_cat,
            method: "GET",
            headers: headersList,
            data: {}
        }

        axios(config)
        .then((response) => {
            let datos = response.data;
            for (let item of datos){
                let itemid = Object.values(item._id);
                this.labelcategoria = itemid[1].toString();
                this.labels.push(itemid[2]);
                this.data.push(+item.Promedio)                     
            }
                        
            const data = {
                labels: this.labels,
                datasets: [{
                    label: this.labelcategoria,
                    data: this.data,
                    fill: true,
                    backgroundColor: 'rgba(230,230,230,0.5)',
                    borderColor: 'rgb(112,179,178)',
                    pointBackgroundColor: 'rgb(112,179,178)',
                    pointBorderColor: '#7BB7AF',
                    pointHoverBackgroundColor: '#E4E4E4',
                    pointHoverBorderColor: 'rgb(126,185,182)',
                }]
            };
            const ctx = document.getElementById('myChart' + id_cat);
            const myChartSub = new Chart(ctx, {
                type: 'radar',
                data: data,
                options: {
                    elements: {
                        line: {
                            borderWidth: 3
                        }
                    },
                    plugins:{
                        legend:{
                            display: false
                        }
                    }
                },
            });
        })
        .finally(() => {
            this.labels = [];
            this.data = [];
        });     
    }

    private getChartTipoLlamada(){
        let headersList = {
            "Accept": "*/*",
            "Content-Type":"application/json",
            "Authorization": 'Basic ' + btoa('usuario1' + ':' + 'usuario1'),
            "Access-Control-Allow-Origin": "http://localhost:9000",
        }

        let config = {
            url: "http://127.0.0.1:9090/tipollamadaget",
            method: "GET",
            headers: headersList,
            data: {}
        }

         axios(config)
        .then((response) => {
            let datos = response.data;
            for (let item of datos){
                let itemid = Object.values(item._id);
                this.labelTipoLlamada = itemid[0].toString();
                this.labels.push(itemid[0]);
                this.data.push(+item.Total)                     
            }
                        
            const data = {
                labels: this.labels,
                datasets: [{
                    label: this.labelTipoLlamada,
                    data: this.data,
                    fill: true,
                    backgroundColor: 'rgba(75, 192, 192, 0.5)',
                    borderColor: 'rgb(75, 192, 192)',
                }]
            };
            
            const ctx = document.getElementById('myChart4');
            const myChartSub = new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    elements: {
                        line: {
                            borderWidth: 3
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins:{
                        legend:{
                            display: false
                        }
                    }
                },
            });
        })
        .finally(() => {
            this.labels = [];
            this.data = [];
        });     
    }
}
</script>