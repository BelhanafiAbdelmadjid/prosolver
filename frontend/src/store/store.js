import { defineStore } from "pinia";

export  const UseAuthStore = defineStore("AuthStore",{

    //state prendra comme valeur une fonction qui retourne un objet qui représente les infos qu'on va stocker
    
    state : () => ({
        userLogged : {
            username : null,
            connexionType : {
                UAT : false,
                PROD : false
            },
            userType : null
        }
    
    }),
    getters : {
        getUsername(){
            return this.username;
        },
        getConnexionType(){
            return this.connexionType;
        }
    },
    actions : {
        setUsername(username){
            this.username = username;
        },
        setConnexionType(connDict){
            this.connexionType(connDict);
        }
    } 
});

