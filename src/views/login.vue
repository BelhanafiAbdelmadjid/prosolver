<template>
    <div v-if="!LogingIn"  class="login-holder" > 
      <div v-if="messageErreur" @click="HideMe"  class="erruer">
        <p>{{ messageErreur }}</p>
      </div>
        <form @submit.prevent="userLogin" class="form_main">
          <p class="heading">Login</p>
          <div class="inputContainer">
                <svg class="inputIcon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#2e2e2e" viewBox="0 0 16 16">
                <path d="M13.106 7.222c0-2.967-2.249-5.032-5.482-5.032-3.35 0-5.646 2.318-5.646 5.702 0 3.493 2.235 5.708 5.762 5.708.862 0 1.689-.123 2.304-.335v-.862c-.43.199-1.354.328-2.29.328-2.926 0-4.813-1.88-4.813-4.798 0-2.844 1.921-4.881 4.594-4.881 2.735 0 4.608 1.688 4.608 4.156 0 1.682-.554 2.769-1.416 2.769-.492 0-.772-.28-.772-.76V5.206H8.923v.834h-.11c-.266-.595-.881-.964-1.6-.964-1.4 0-2.378 1.162-2.378 2.823 0 1.737.957 2.906 2.379 2.906.8 0 1.415-.39 1.709-1.087h.11c.081.67.703 1.148 1.503 1.148 1.572 0 2.57-1.415 2.57-3.643zm-7.177.704c0-1.197.54-1.907 1.456-1.907.93 0 1.524.738 1.524 1.907S8.308 9.84 7.371 9.84c-.895 0-1.442-.725-1.442-1.914z"></path>
                </svg>
            <input  v-model="username" type="text" class="inputField" id="username" placeholder="Username">
            </div>
            
            <div class="inputContainer">
                <svg class="inputIcon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#2e2e2e" viewBox="0 0 16 16">
                <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"></path>
                </svg>
                <input v-model="password" type="password" class="inputField" id="password" placeholder="Password">
            </div>


                            
            <div class="Choice">
                <select  v-model="ServerType" >
                <option  v-for="option , index in options" :value="option" :key="index">{{ option }}</option>
              </select>
            </div>
                        
            <button id="button">Submit</button>

        </form>
              
    </div>
    <loading class="containerAnimation" v-else ></loading>

</template>
<script>

import { UseAuthStore } from "@/store/store.js"
import apiFetch from "@/common/api.service.js"

import loading from "@/components/loadingAnimations/dot-animation.vue"


export default{
    name :'login-vue',
    data(){
      return{
        AuthStore : UseAuthStore(),
        messageErreur : null,
        username : "",
        password : "",
        serveurs : null,
        ServerType : "UAT",
        options : ["Prod","UAT"],
        LogingIn : false,
      }
    },
    methods : {
      async userLogin(){
        if(this.ServerType == null){
          this.messageErreur = "Please select a server type.";
          return ;
        }
        this.LogingIn = true;
        let endpoint = "/" + this.ServerType+'/login';
        apiFetch.post(endpoint,{"username" :  this.username , "password" : this.password},false,true)
        .then( (response)=>{
          console.log(response);
          this.AuthStore.setUsername = this.username;
          this.AuthStore.setConnexionType = {
              UAT : this.ServerType == 'Pord' ? false : true,
              PROD : this.ServerType == 'Pord' ? true : false,
          };
          var query ={};
           if(this.ServerType == 'UAT'){
            query = {
              UAT : true
            }
           }else{
            query = {
              Prod : false
            }
           }
          this.$router.push({name : 'supervision' , query : { ...query }});
        })
        .catch( (error)=>{
          console.log(error)
          this.LogingIn = false;
          this.messageErreur = error.msg;
        });
      },

      HideMe(){
        this.messageErreur = null;
      },
      checkLogin(){
        let endpoint = "/UAT/logedin";
        apiFetch.get(endpoint,false)
        .then((response)=>{
          this.AuthStore.username = response.username;
          this.AuthStore.connexionType = {
            UAT : true,
            Prod : false
          };
          if(response.status.ok){
            this.$router.push({name : 'supervision' , query : { UAT :  true  }});
          }
        })
        .catch((error)=>{
            // this.$router.push("/Server-Down");
            console.log(error)
        })
      }
    },
    mounted(){
      this.checkLogin();
    },
    components: {
      loading
  },
  setup(){

  }

}
</script>
<style scoped >
.erruer{
  position: absolute;

  display: flex;
  justify-content: center;
  align-items: center;

  width: 100%;

  left: 0;
  top: 0;

  background-color: rgb(235, 72, 72);
  color:var( --white-text-color);
  font-weight : 500;

  padding: 5px;
  box-sizing: border-box;
}
.login-holder{
  position:fixed;
  top:0;
  left: 0;
  z-index: 99999;

  height: 100vh;
  width: 100vw;
  background-color: var( --background-color);

  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;

    
}
.form_main {
  width: 220px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: var(--light-color-0);
  padding: 30px 30px 30px 30px;
  box-shadow: 0px 0px 40px rgba(0, 0, 0, 0.062);
  position: relative;
  overflow: hidden;
}

.form_main::before {
  position: absolute;
  content: "";
  width: 300px;
  height: 300px;
  background-color: var(--light-color-1);
  transform: rotate(45deg);
  left: -180px;
  bottom: 30px;
  z-index: 1;
  border-radius: 30px;
  box-shadow: 5px 5px 10px #00000015;
}

.heading {
  font-size: 2em;
  color: var(--dark-text-color);
  font-weight: 700;
  margin: 5px 0 10px 0;
  z-index: 2;
}

.inputContainer {
  width: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}

.inputIcon {
  position: absolute;
  left: 3px;
}

.inputField {
  width: 100%;
  height: 30px;
  background-color: transparent;
  border: none;
  border-bottom: 2px solid rgb(173, 173, 173);
  margin: 10px 0;
  color: var(--dark-text-color);
  font-size: .8em;
  font-weight: 500;
  box-sizing: border-box;
  padding-left: 30px;
}

.inputField:focus {
  outline: none;
  border-bottom: 2px solid rgb(199, 114, 255);
}

.inputField::placeholder {
  color: var(--gray-text-color-1);
  font-size: 1em;
  font-weight: 500;
}

#button {
  z-index: 2;
  position: relative;
  width: 100%;
  border: none;
  background-color: var( --warm-color-0);
  height: 30px;
  color: var(--white-text-color);
  font-size: .8em;
  font-weight: 500;
  letter-spacing: 1px;
  margin: 10px;
  cursor: pointer;
}

#button:hover {
  background-color: var(--warm-color-1 );
}

.Choice{
  width: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  z-index: 2;

}
</style>