import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router';
// import BootstrapVue from 'bootstrap-vue';
import Keycloak, { KeycloakOnLoad } from 'keycloak-js';
import i18n from './i18n'
import vuetify from './plugins/vuetify';

// import 'bootstrap/dist/css/bootstrap.css';
// import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.config.productionTip = false
Vue.config.devtools = true
// Vue.use(BootstrapVue);

// const currentHostname = window.location.hostname; 
let urls;

// console.log("'-->log: Hostname " + currentHostname );
// console.log("'-->log: VUE_APP_KEYCLOAK " + window.VUE_APP_KEYCLOAK);
// console.log("'-->log: VUE_APP_ROOT " + window.VUE_APP_ROOT);

// if (currentHostname.indexOf('localhost') > -1) {
//   console.log("--> log: option 1");
//   urls = {
//     api: 'http://localhost:8082',  
//     login: 'http://localhost:8282/auth', 
//     cns: 'http://localhost:8080' // Verify the shown ports
//   }
//   store.commit("setAPIAndLogin", urls);
// }
// else {
//   console.log("--> log: option 2");
//   const keycloakUrl = window.VUE_APP_KEYCLOAK;
//   const webapiUrl = window.VUE_APP_WEBAPI;
//   const cnsRedirectUrl = 'https://' + currentHostname + window.VUE_APP_ROOT; // logout
//   urls = {
//     api: webapiUrl,
//     login: keycloakUrl,
//     cns: cnsRedirectUrl 
//   }
//   console.log("--> log: urls ", urls);
//   store.commit("setAPIAndLogin", urls);
// }

// console.log("--> log: webapiUrl : " +  urls.webapiUrl);
// console.log("--> log: keycloakUrl : " + urls.keycloakUrl);

const initOptions = {
  url: process.env.VUE_APP_KEYCLOAK_URL, 
  realm: process.env.VUE_APP_KEYCLOAK_REALM, 
  clientId: process.env.VUE_APP_KEYCLOAK_CLIENT, 
  onLoad: "login-required" as KeycloakOnLoad
}

const keycloak = Keycloak(initOptions);

keycloak.init({ onLoad: initOptions.onLoad }).then(( auth : any ) => {
  
  if (!auth) {
    window.location.reload();
  }
  else{
    console.log("Authenticated");

    new Vue({
      el: '#app',
      router,
      store,
      vuetify,
      i18n,
      render: h => h(App, { props: { keycloak: keycloak } })
    })
  }
  

  // localStorage.setItem('rol',keycloak.resourceAccess.xentric_base.roles )
  // localStorage.setItem('token', keycloak.token );

  // console.log( keycloak.token );

  let payload: any = {
    idToken: keycloak.idToken,
    accessToken: keycloak.token
  }

  if(( keycloak.token && keycloak.idToken != '' ) && (keycloak.idToken != '')){

    store.commit("login", payload)
    
    payload = { name: keycloak.tokenParsed.preferred_username }
    store.commit("setName", payload)
    
  }else{

    const payloadRefreshedTokens = {
      idToken: "",
      accessToken: ""
    }
    store.commit("login", payloadRefreshedTokens);
    store.commit("logout");
  }

  setInterval(() => {
    keycloak.updateToken(70).then((refreshed) => {
      
      if (store.state.user.isAuthenticated != false ) {
        if (refreshed) {        
          let payloadRefreshedTokens = {
            idToken: keycloak.idToken,
            accessToken: keycloak.token
          }

          if ((keycloak.token && keycloak.idToken != '') && (keycloak.idToken != '')) {
            store.commit("login", payloadRefreshedTokens);
          }
          else {
            console.log("--> log: token refresh problems");  
            payloadRefreshedTokens = {
              idToken: "",
              accessToken: ""
            }
            store.commit("login", payloadRefreshedTokens);
            store.commit("logout");
          }
        }
      } else {
        console.log("--> log: logout isAuthenticated  =", store.state.user.isAuthenticated);
        
        const logoutOptions = { redirectUri : 'http://localhost:9000/' };

        keycloak.logout(logoutOptions).then((success) => {

              localStorage.removeItem('rol')
              console.log("--> log: logout success ", success );

        }).catch((error) => {
          
              console.log("--> log: logout error ", error );
        });
        store.commit("logout");
      }
      
    }).catch(() => {
      console.log("--> log: catch interval");
    });
  }, 1000)

}).catch(() => {
  //Vue.$log.error("Authenticated Failed");
  console.log("Authenticated Failed");
});