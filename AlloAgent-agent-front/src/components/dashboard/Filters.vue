<template>
    <v-container class="mb-5">
        <v-row>
            <v-col lg="2" md="3" sm="6" cols="6">
                <v-menu 
                v-model="menu1" :close-on-content-click="false" :nudge-right="40" lazy transition="scale-transition" offset-y full-width min-width="290px" elevation="12">
                    <template v-slot:activator="{ on }">
                        <v-text-field v-model="date1" label="Desde" prepend-icon="mdi-calendar" readonly v-on="on"/>
                    </template>
                    <v-date-picker v-model="date1" @input="menu1 = true"/>
                </v-menu>       
            </v-col>

            <v-col lg="2" md="4" sm="6" cols="6">
                <v-menu v-model="menu2" :close-on-content-click="false" :nudge-right="40" lazy transition="scale-transition" offset-y full-width min-width="290px" elevation="12">
                    <template v-slot:activator="{ on }">
                        <v-text-field v-model="date2" label="Hasta" prepend-icon="mdi-calendar" readonly v-on="on"></v-text-field>
                    </template>
                    <v-date-picker v-model="date2" @input="menu2 = true"/>
                </v-menu>  
            </v-col>
            
            <v-col lg="2" md="4" sm="6" cols="6">
                <v-select v-model="selectcampania" :items="itemscampania" filled item-text="id" item-value="abbr" label="Campaña" single-line></v-select>
            </v-col>

            <v-col lg="2" md="4" sm="6" cols="6">
                <v-select v-model="selecttipo" :items="itemstipo" filled label="Tipo de llamada"></v-select>
            </v-col>

            <v-col lg="2" md="1" cols="6" class="d-flex my-3">
                <v-btn v-on:click='filtertable' color="#06B7B2" class="font-weight-bold white--text mr-2">Filtrar<v-icon color="white">mdi-magnify</v-icon></v-btn>
                <v-btn @click="downloadWithCSS" color="#06B7B2" class="font-weight-bold white--text mr-2">Descargar</v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>


<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { internet } from '@/utils/Internet';
import { IDataTable } from '@/model/main/IDataTable';
import { IHeaderTable } from '@/model/main/IHeaderTable';
import { AxiosResponse } from 'axios';
import Util from '@/utils/Util';
import { ILabels } from '@/model/labels/ILabelsEvaluacion';
import axios from "axios";
import DataTable from '@/components/dashboard/DataTable.vue'
import { jsPDF } from "jspdf";
import domtoimage from 'dom-to-image';

@Component({
    name: 'Filters',
})

export default class Filters{
    public menu1 = false;
    public menu2 = false;
    public date1 = "";
    public date2 = "";
    public selectcampania = 'Todos';
    public selecttipo = 'Todos';
    public itemscampania = ['Todos'];
    public itemstipo = ['Todos'];
    public campania = 'Todos';
    public fechai = "";
    public fechaf = "";

    mounted(): void {
        this.getCampania();
		this.getTipoLlamada();
    }

    public async filtertable(){
        let campania = this.selectcampania;
        let fecha1 = this.date1;
        let fecha2 = this.date2;

        if (fecha1 == '' || fecha2 == ''){
            await alert('Seleccionar ambas fechas antes de filtrar!')
        }
        else{
            let dT = new DataTable();
            dT.getData(campania, fecha1, fecha2);
        }

    }

    private getCampania(){

        let headersList = {
        "Accept": "*/*",
        "Content-Type":"application/json",
        "Authorization": 'Basic ' + btoa('usuario1' + ':' + 'usuario1'),
        "Access-Control-Allow-Origin": "http://localhost:9000",
        }

        let config = {
            url: "http://127.0.0.1:9090/campaniaget",
            method: "GET",
            headers: headersList,
            data: {}
        }

        axios(config)
        .then((response) => {
            let datos = response.data;
            for (let item of datos){
                for (let i of item.distinctcampanias){					
                    this.itemscampania.push(i)
                }	 			
            }
        })
    }

    private getTipoLlamada(){

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
                this.itemstipo.push(itemid[0]);
            }
        })
    }

    public downloadWithCSS(){
        const dashboard = document.querySelector('#dashboard_main')
        console.log(dashboard)
        domtoimage
        .toPng((dashboard)!)
        .then(function(dataUrl: any) {
            console.log(dataUrl)
            let img = new Image();
            img.src = dataUrl;
            img.onload = function () {
                let doc :any =''
                console.log("img:", img.width,  img.height)

                if (img.width > img.height) {
                    doc = new jsPDF('l', 'mm', [img.width, img.height])
                }else{
                    doc = new jsPDF('p', 'mm', [img.width, img.height])
                }   
                doc.addImage (img, 'jpeg', 10, 10, img.width, img.height)

                const date = new Date();
                    const filename =
                        "dashboard - " +
                        date.getFullYear() +
                        ("0" + (date.getMonth() + 1)).slice(-2) +
                        ("0" + date.getDate()).slice(-2) +
                        ("0" + date.getHours()).slice(-2) +
                        ("0" + date.getMinutes()).slice(-2) +
                        ("0" + date.getSeconds()).slice(-2) +
                        ".pdf";
                    doc.save(filename);
            };
        })
        .catch(function(error: any) {
            console.error("oops, something went wrong!", error);
        });   
    }
}
</script>