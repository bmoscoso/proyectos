<template>
    <div>
        <v-container class="mt-5"> 
            <v-row>
                <v-col>
                    <v-data-table
                        name="evaluations"
                        :key="componentKey"
                        :headers="header"
                        :items="rows"
                        class="elevation-1">
                        <template v-slot:item="row">
                            <tr color="red">
                                <td>{{row.item.MT_Folio}}</td>
                                <td>{{row.item.FechaGestion}}</td>
                                <td align: center>{{row.item.Categoria1}}</td>
                                <td align: center>{{row.item.Categoria2}}</td>
                                <td align: center>{{row.item.Categoria3}}</td>
                                <td><v-icon large mr-2 @click="openDetails(row.item)">mdi-file-document-multiple-outline</v-icon></td>
                            </tr>
                        </template>
                    </v-data-table>
                </v-col>  
            </v-row>	
        </v-container>

        <v-dialog
            v-model="dialogDetails"
            width="auto"
            persistent
            >
            <v-card>
                <div style="overflow-x: hidden; overflow-y: hidden;">
                    <v-row justify="center"> 
                        <v-col>
                            <div class="pt-5 px-5">
                                <audio id="audio" src="@/audios/AIEP01_20200210-170849_56978277387_451_78295597-all.wav" controls></audio>
                            </div>
                            <v-card-title primary-title>                                
                            </v-card-title> 
                            <v-data-table
                                name="evaluationsDetails"
                                :headers="headerDetails"
                                :items="rowDetails"
                                class="elevation-1">
                                <template v-slot:item="row">
                                    <tr>
                                        <td>{{row.item.MT_Folio}}</td>
                                        <td>{{row.item.campania}}</td>
                                        <td>{{row.item.categoria}}</td>
                                        <td>{{row.item.subcategoria}}</td>
                                        <td>{{row.item.elemento_explicito}}</td>
                                        <td>{{row.item.Encontrado}}</td>
                                        <td><v-icon large mr-2 @click="openEmail(row.item)">mdi-email-edit-outline</v-icon></td>
                                    </tr>
                                </template>
                            </v-data-table>
                            <v-card-actions>
                                <v-btn color="red" @click="dialogDetails = false" text>Cerrar</v-btn>		
                            </v-card-actions>
                        </v-col>
                    </v-row>
                </div>               
            </v-card>
        </v-dialog>


        <v-dialog v-model="dialogEmail" width="30%" persistent>
            <v-card  style="overflow-x: hidden; overflow-y: hidden;">
                <v-row justify="center">
                    <v-col>
                        <v-card-title primary-title>
                            Comentario
                        </v-card-title> 
                        <v-card>
                            <form>
                                <v-col>
                                    <v-text-field
                                    v-model="elementEmail"
                                    label="supervisor@test.com"
                                    required
                                    >
                                    <v-textarea>
                                    </v-textarea>
                                    </v-text-field>
                                </v-col>
                                <v-col>
                                    <v-text-field
                                    v-model="elementSub" 
                                    label="Subcategoria"
                                    required
                                    disabled
                                    >
                                    <v-textarea>
                                    </v-textarea>
                                    </v-text-field>
                                </v-col>
                                <v-container fluid>
                                    <v-textarea
                                    v-model="elementMessage"
                                    autocomplete="Mensaje"
                                    label="Mensaje"
                                    ></v-textarea>
                                </v-container>
                                <v-card-actions>
                                    <v-btn color="red" @click="dialogEmail = false" text>CERRAR</v-btn>
                                    <v-btn type="submit" color="#26c6da" @click="sendEmail()" text>ENVIAR</v-btn>
                                </v-card-actions>
                            </form>
                        </v-card>
                    </v-col>
                </v-row>
            </v-card>
        </v-dialog>
    </div>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';
    import { IDataTable } from '@/model/main/IDataTable';
    import { IHeaderTable } from '@/model/main/IHeaderTable';
    import { AxiosResponse } from 'axios';
    import Util from '@/utils/Util';
    import { ILabels } from '@/model/labels/ILabelsEvaluacion';
    import axios from "axios";
    import emailjs from 'emailjs-com';

    @Component({
        name: 'DataTable',
        
        methods: {
            sendEmail() {
                let SERVICE_ID = 'service_815a1hs';
                let TEMPLATE_ID = 'template_chg8qkk';
                let USER_ID = 'YJEKmrDbOoHCa5cUE';
                try {
                    emailjs.send(
                        SERVICE_ID, 
                        TEMPLATE_ID, {
                            message: this.elementMessage,
                            folio: this.elementFolio,
                            subcategory: this.elementSub,
                            email: this.elementEmail,
                        },
                        USER_ID,
                    )
                } catch(error) {
                    console.log({error})
                }
                // Reset form field
                this.elementEmail = ''
                this.elementSub = ''
                this.elementMessage = ''
                this.dialogEmail = false
            },
        },
    })

    export default class DataTable extends Vue{
        public rows: Array<IDataTable> = [];
        public header: Array<IHeaderTable<IDataTable>> = [];
        public rowDetails: Array<IDataTable> = [];
        public headerDetails: Array<IHeaderTable<IDataTable>> = [];
        public isLoading = false;
        public ilabels: Array<ILabels> = [];
        public dialog = false;     
        public dialogDetails = false; 
        public dialogEmail = false; 
        public componentKey = 0;
        public esubcategoria = '';
        public elementEmail ='';
        public elementSub = '';
        public elementMessage = '';
        public elementFolio = '';
        public audioGet = '';

        mounted(): void {
            this.getData('','','');
        }

        public getData(campania:string, fechai: string, fechaf: string) {

            this.isLoading = true;
            this.dialogDetails = false;
            
            if (campania == '' && fechai == '' && fechaf == ''){
                campania = 'Todos';
                fechai = '2005-01-01';
                fechaf = '2050-12-31'
            }
            let headersList = {
                "Accept": "*/*",
                "Content-Type":"application/json",
                "Authorization": 'Basic ' + btoa('usuario1' + ':' + 'usuario1'),
                "Access-Control-Allow-Origin": "http://localhost:9000",
            }
            let config = {
                url: "http://127.0.0.1:9090/evaluacion?campania="+ campania + '&fechai=' + fechai + '&fechaf=' + fechaf,
                method: "GET",
                headers: headersList,
                data: {}
            }
            
            axios(config)
            .then((response) => {
                let datos = response.data
                this.ilabels = datos;
                const dataTable: Array<IDataTable> = [];
                let ptje1 = '0';
                let ptje2 = '0';
                let ptje3 = '0';
                for (let item = 0; item < this.ilabels.length; item++) {
                    let itemid = Object.values(this.ilabels[item]._id);			
                    let folio = itemid[0];		
                    let cat = itemid[3];			
                    switch(cat){
                        case '1':
                            ptje1 = this.ilabels[item].Ponderacion;
                            break;
                        case '2':
                            ptje2 = this.ilabels[item].Ponderacion;
                            break;
                        case '3':
                            ptje3 = this.ilabels[item].Ponderacion;
                            break;
                    }
                    try{
                        let itemidnext = Object.values(this.ilabels[item+1]._id);
                        if (folio === itemidnext[0]){					
                            continue;
                        }
                        else{
                            const row: IDataTable = {};
                            row['MT_Folio'] = itemid[0];
                            row['FechaGestion'] = itemid[1];
                            row['Categoria1'] = ptje1 + '%';
                            row['Categoria2'] = ptje2 + '%';
                            row['Categoria3'] = ptje3 + '%';					
                            row['Detalle'] = "";
                            dataTable.push(row);
                            ptje1 = '0';
                            ptje2 = '0';
                            ptje3 = '0';
                        }
                    }
                    catch{
                        const row: IDataTable = {};
                        row['MT_Folio'] = itemid[0];
                        row['FechaGestion'] = itemid[1];
                        row['Categoria1'] = ptje1 + '%';
                        row['Categoria2'] = ptje2 + '%';
                        row['Categoria3'] = ptje3 + '%';
                        row['Detalle'] = "";
                        dataTable.push(row);
                        ptje1 = '0';
                        ptje2 = '0';
                        ptje3 = '0';
                    }
                }
                const header: Array<IHeaderTable<
                    IDataTable
                >> = Object.keys(dataTable[0]).map(
                    (
                        key: string
                    ): IHeaderTable<IDataTable> => {
                        let text = key;
                        switch (key) {
                            case 'MT_Folio':
                                text = "Folio";
                                break;
                            case 'FechaGestion':
                                text = "Fecha Gestion";
                                break;
                            case 'Categoria1':
                                text = "Ptje. Categoria 1";
                                break;
                            case 'Categoria2':
                                text = "Ptje. Categoria 2";
                                break;
                            case 'Categoria3':
                                text = "Ptje. Categoria 3";
                                break;
                        }
                        return {
                            text,
                            align: 'center',
                            value: key,
                        };
                    }) as Array<IHeaderTable<IDataTable>>;
                    this.rows = dataTable;
                    this.header = header;
                    })
                .catch(console.log)
                .finally(() => {
                this.isLoading = false; 
                this.componentKey += 1;
                });
            }

        public getDetails(folio:string){

            this.isLoading = true;

            let headersList = {
                    "Accept": "*/*",
                    "Content-Type":"application/json",
                    "Authorization": 'Basic ' + btoa('usuario1' + ':' + 'usuario1'),
                    "Access-Control-Allow-Origin": "http://localhost:9000",
                }

            let config = {
                url: "http://127.0.0.1:9090/evaluaciondetail?folio=" + folio,
                method: "GET",
                headers: headersList,
                data: {},
            }

            axios(config)
            .then((response) => {
                let datos = response.data
                this.ilabels = datos;
                const dataTable: Array<IDataTable> = [];
                for (let item of this.ilabels) {
                    const row: IDataTable = {};
                    let itemid = Object.values(item._id);
                    row['MT_Folio'] = itemid[0];
                    row['campania'] = itemid[1];
                    row['categoria'] = itemid[4];
                    row['subcategoria'] = itemid[5]
                    row['elemento_explicito'] = itemid[6];
                    row['Encontrado'] = item.Encontrado;
                    this.audioGet = itemid[7];
                    dataTable.push(row);
                }
                const header: Array<IHeaderTable<
                    IDataTable
                >> = Object.keys(dataTable[0]).map(
                    (
                        key: string
                    ): IHeaderTable<IDataTable> => {
                        let text = key;
                        switch (key) {
                            case 'MT_Folio':
                                text = "Folio";
                                break;
                            case 'campania':
                                text = "Campaña";
                                break;
                            case 'categoria':
                                text = "Categoria";
                                break;
                            case 'subcategoria':
                                text = "Subcategoria";
                                break;
                            case 'elemento_explicito':
                                text = "Elemento";
                                break;
                            case 'Encontrado':
                                text = "Encontrado";
                                break;
                        }
                        return {
                            text,
                            value: key,
                        };
                    }) as Array<IHeaderTable<IDataTable>>;
                this.rowDetails = dataTable;
                this.headerDetails = header;
            })
            .catch(console.log)
            .finally(() => {
            this.isLoading = false;
            });
        }

        public openDetails(item:ILabels){
            let currentFolio = item.MT_Folio;
            this.dialogDetails = true;
            this.getDetails(currentFolio)
        }

        public openEmail(item:ILabels){
            this.dialogEmail = true;
            this.elementSub = item.subcategoria
            this.elementFolio = item.MT_Folio;
        }
    }
</script>
<style>
#audio{
    width: 100%;
}
</style>