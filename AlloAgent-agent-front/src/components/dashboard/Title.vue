<template>
    <v-row col="10">
        <v-col col="12" class="py-0 mt-3">
            <v-container>
                <v-card :elevation="2" class="mx-auto d-flex align-start my-0 mb-6">
                    <v-col lg="12" class="ml-3 d-flex align-start">
                        <v-img contain src="@/assets/Alloxentric-logomark.png" max-width ="60" class="pa-0">
                        </v-img>
                        <h2 class="pa-0 my-3 ml-2">Dashboard</h2>
                    </v-col>
                </v-card>
            </v-container>
        </v-col>
    </v-row>
</template>

<script lang="ts">
    import { Component, Vue } from 'vue-property-decorator';

@Component({
    name: 'Title',
})

    export default class Title{

    }

</script>