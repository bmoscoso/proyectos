<template>
    <v-container>
        <v-row justify="center">
            <v-col lg="3" md="6" sm="6" cols="12">
                <v-card class="mx-auto" elevation="2">
                    <v-list-item three-line>
                    <v-list-item-content>
                        
                        <div class="text-overline mb-4 d-flex justify-space-between" cols="6">
                            <h4 class="my-5">SALUDO</h4>
                            <v-list-item-avatar><v-icon x-large>mdi-hand-back-right-outline</v-icon></v-list-item-avatar>
                        </div>
                        
                        <v-progress-linear 
                        :value="cardSaludo" 
                        color="teal accent-3" 
                        height="25" 
                        striped>
                            <template v-slot:default="{ value }" >
                                <div> Avance
                                    <strong>{{ Math.ceil(value) }}%</strong> 
                                </div>
                            </template>
                        </v-progress-linear>
                        <v-divider class="my-2"></v-divider>

                        <div class="mt-3">
                            Total de registros: {{ this.total }}
                        </div>
                    </v-list-item-content>
                    </v-list-item>
                </v-card>
            </v-col>

            <v-col lg="3" md="6" sm="6" cols="12">
                <v-card class="mx-auto" elevation="2">
                    <v-list-item three-line>
                    <v-list-item-content>
                        
                        <div class="text-overline mb-4 d-flex justify-space-between" cols="6">
                            <h4 class="my-5">OBJETIVO</h4>
                            <v-list-item-avatar><v-icon x-large>mdi-phone-check-outline</v-icon></v-list-item-avatar>
                        </div>
                        
                        <v-progress-linear 
                        :value="cardObjetivo" 
                        color="teal accent-3" 
                        height="25" 
                        striped>
                            <template v-slot:default="{ value }">
                                <div> Avance
                                    <strong>{{ Math.ceil(value) }}%</strong>
                                </div>
                            </template>
                        </v-progress-linear>
                        <v-divider class="my-2"></v-divider>

                        <div class="mt-3">
                            Total de registros: {{ this.total }}
                        </div>
                    </v-list-item-content>
                    </v-list-item>
                </v-card>
            </v-col>

            <v-col lg="3" md="6" sm="6" cols="12">
                <v-card class="mx-auto" elevation="2">
                    <v-list-item three-line>
                    <v-list-item-content>
                
                        <div class="text-overline mb-4 d-flex justify-space-between" cols="6">
                            <h4 class="my-5">CIERRE</h4>
                            <v-list-item-avatar><v-icon x-large>mdi-hand-wave-outline</v-icon></v-list-item-avatar>
                        </div>
                        
                        <v-progress-linear 
                        :value="cardCierre" 
                        color="teal accent-3" 
                        height="25" 
                        striped 
                        active>
                            <template v-slot:default="{ value }">
                                <div> Avance
                                    <strong>{{ Math.ceil(value) }}%</strong>
                                </div>
                            </template>
                        </v-progress-linear>
                        <v-divider class="my-2"></v-divider>

                        <div class="mt-3">
                            Total de registros: {{ this.total }}
                        </div>
                    </v-list-item-content>
                    </v-list-item>
                </v-card>
            </v-col>

            <v-col lg="3" md="6" sm="6" cols="12">
                <v-card class="mx-auto" elevation="2">
                    <v-list-item three-line>
                    <v-list-item-content>
                        
                        <div class="text-overline mb-4 d-flex justify-space-between" cols="6">
                            <h4 class="my-5">TAS</h4>
                            <v-list-item-avatar><v-icon x-large>mdi-archive-check-outline</v-icon></v-list-item-avatar>
                        </div>
                        
                        <v-progress-linear 
                        :value="cardTAS" 
                        color="teal accent-3" 
                        height="25" 
                        striped>
                            <template v-slot:default="{ value }">
                                <div> Avance
                                    <strong>{{ Math.ceil(value) }}%</strong>
                                </div>
                            </template>
                        </v-progress-linear>
                        <v-divider class="my-2"></v-divider>

                        <div class="mt-3">
                            Total de registros: {{ this.total }}
                        </div>
                    </v-list-item-content>
                    </v-list-item>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';
    import axios from "axios";  

    
    @Component({
        name: 'Card'
    })
    
    export default class Card{

        public cardSaludo = 0;
        public cardObjetivo = 0;
        public cardCierre = 0;
        public cardTAS = 0;
        public total = 0;

        mounted(): void{
            this.getCards()
        }

        public getCards(){

            let headersList = {
            "Accept": "*/*",
            "Content-Type":"application/json",
            "Authorization": 'Basic ' + btoa('usuario1' + ':' + 'usuario1'),
            "Access-Control-Allow-Origin": "http://localhost:9000",
            }

            let config = {
                url: "http://localhost:9090/cardsget",
                method: "GET",
                headers: headersList,
                data: {}
            }

            axios(config)
            .then((response) => {
                let datos = response.data;
                for (let item of datos){
                    let itemid = Object.values(item._id);	
                    let cat = itemid[0];
                    switch(cat){
                        case '1':
                            this.cardSaludo = +item.Promedio;
                            break;
                        case '2':
                            this.cardObjetivo = +item.Promedio;
                            break;
                        case '3':
                            this.cardCierre = +item.Promedio;
                            break;
                    }
                    this.total = item.Total
                }
                this.cardTAS = (this.cardSaludo + this.cardObjetivo + this.cardCierre)/3
            })
        }
    }
</script>