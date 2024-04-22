<template>
    <largeNavBar v-if="widthLarge" :connexionType="connexionType" :userType="AuthStore.userType" @logout="logout" ></largeNavBar>
    <thinNavBar v-else  :connexionType="connexionType"  :userType="AuthStore.userType" @logout="logout"></thinNavBar>
</template>
<script>
import thinNavBar from './thin-nav-bar.vue';
import largeNavBar from './large-nav-bar.vue';

import { UseAuthStore } from '@/store/store';
import apiFetch from '@/common/api.service';
export default{
    data(){
        return {
            AuthStore : UseAuthStore(),
            widthLarge : window.innerWidth >= 1000 ? true : false,
            connexionType : null
        }
    },
    mounted(){
        window.addEventListener('resize', ()=>{
            this.widthLarge = window.innerWidth >= 1000 ? true : false;
        });
    },
    components : {
        thinNavBar,
        largeNavBar
    },
    created(){
        let endpoint = "/login/informations"
        apiFetch.get(endpoint,false)
        .then((response)=>{
            this.AuthStore.username = response.username;
            this.AuthStore.connexionType = response.connexionType;
            this.AuthStore.userType = response.userType;
            console.log(this.AuthStore.userType)

            this.connexionType = response.connexionType.UAT == true ? 'UAT' : 'Prod'
        })
    },
    methods : {
        logout(){
            let endpoint = "/disconnect"
            apiFetch.post(endpoint,{},false,true)
            .then(()=>{
                this.$router.push({name : 'login'})
            })
            .catch((err)=>{
                console.log(err)
            })
        }
    }
}
</script>
