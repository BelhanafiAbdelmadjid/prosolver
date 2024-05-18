/* -------------------------------------------------------------------------- */
/*                                  JSON DATA                                 */
/* -------------------------------------------------------------------------- */
/*  

servers : Array
[
{
    id : X , name : "test" , ip : "@ip" , status : "Active/Down" , containers : [{ id : "" , name : "" , ports : '',status : '' }]
}
]

/* -------------------------------------------------------------------------- */
/*                                    TO DO                                   */
/* -------------------------------------------------------------------------- */

Methods : (getServers) , getServersWithNameLike

*/
<template>
  <div class="holders hoder-supervision">
    <div class="Welcomeback colorfull-gradient-1">
      <h1>Welcome back, {{AuthStore.username}}!👋</h1>
      <p>How things are going today?</p>
    </div>
    <queryNavbar @input-changed="onInputChanged" :theme="'white'">
      <template #Title>
        Servers {{ " "+ (this.$route.query.UAT ? "UAT" : "Prod" ) }}
      </template>
    </queryNavbar>
    <tableExtension>
      <template #tableHeaders>
        <td>Name</td>
        <td>IP</td>
        <td>Status</td>
      </template>
      <template #tableRows>
        <tr  v-for="server in servers" :key="server.id" @click="displayContainersOf(server)">
          <td class="server-name">{{ server.name }}</td>
          <td>
            <p>{{ server.ip }}</p>
          </td>
          <td>
            <p class="holder-status">
              <span
                :class="{ 'status-dot-active' : server.status == 'Active','status-dot-down' : server.status == 'Down'  }"
                class="status-dot"></span>
              <span>{{ server.status }}</span>
            </p>
          </td>
        </tr>
      </template>
      <template #tableLoadingAnimation >
        <loadingBar style="width: 100%;" v-if="fetchingForServers == true" ></loadingBar>
        <p v-if="fetchingForServers == false && servers.length == 0" >No matching server was found...</p>
      </template>

    </tableExtension>

    <popupDisplay style="width: 100%;height: 100%;"  v-if="displayContainersOnPopUp == true"
      @close-popup="displayContainersOnPopUp = false; containersPopUpDisplay = null">
      <template #titel >
        Containers
      </template>
      <template #content >
        <div v-if="containersPopUpDisplay != null" class="popup-holder">
          <div class="container-list-holder" v-if="containersPopUpDisplay.length != 0" >
            <tableExtension >
            <template #tableHeaders>
              <td>Name</td>
              <td>ID</td>
              <td>PORTS</td>
              <td>STATUS</td>
            </template>
            <template #tableRows>
              <tr v-for="container in containersPopUpDisplay" :key="container.id">
                <td class="server-name">{{ container["NAMES"] }}</td>
                <td>
                  <p>{{ container["CONTAINER ID"] }}</p>
                </td>
                <td>
                  <p>{{ container["PORTS"] }}</p>
                </td>
                <td>
                  <p>{{ container["STATUS"] }}</p>
                </td>
              </tr>
            </template>
            </tableExtension>
          </div>

          <p v-else >This server has no runing container...</p>
        </div>
        <loadingBar v-if="containersPopUpDisplay == null" ></loadingBar>
      </template>
    </popupDisplay>
  </div>
</template>
<script>
import { UseAuthStore } from "@/store/store.js"
import apiFetch from "@/common/api.service.js"

import popupDisplay from "@/components/interraction/popups/popup-display.vue"
import queryNavbar from "@/components/interraction/query/query-navbar.vue"
import tableExtension from "@/components/interraction/tables/table-withextension.vue"
import loadingBar from "@/components/loadingAnimations/bar-loading.vue"
export default{
    name : 'supervision-view',
    data(){
        return{
          AuthStore : UseAuthStore(),
          servers : [],
          fetchingForServers : true,
          displayContainersOnPopUp : false,
          containersPopUpDisplay : null
        } 
    },
    components : {
      queryNavbar,
      tableExtension,
      popupDisplay,
      loadingBar,
    },
    methods : {
      getServers(query_name){
        this.fetchingForServers= true;
        let type = this.$route.query.UAT ? 'UAT' : 'Prod' ;
        let endpoint = "/" + type +'/servers';
        if(query_name != null){
          endpoint = endpoint + "?name=" + query_name
        }
        apiFetch.get(endpoint,false)
        .then( (servers)=>{
          this.servers = servers;
          this.fetchingForServers=false;
          if(query_name != null && servers.length == 0){
            this.emitter.emit("sidebar-error",{error : true , description : "No server matching "+query_name+" was found."})
          }
        })
      },
      onInputChanged(inputValue){
        this.getServersWithNameLike(inputValue)
      },
      getServersWithNameLike(NameLike){
        console.log(NameLike)
        this.getServers(NameLike)
      },
      displayContainersOf(server){
        //api/server/<int:server>/containers
        let endpoint = "/server/" + server.id +'/containers/status';
        apiFetch.get(endpoint,false,true)
        .then( (containers)=>{
          this.containersPopUpDisplay = containers;
        })
        .catch((error)=>{
          this.displayContainersOnPopUp = false;
          this.containersPopUpDisplay = null;
          this.emitter.emit("sidebar-error",{error : true , description : error.error})
        })

        this.displayContainersOnPopUp = true;
      },
      addHashToLocation(params) {
        history.pushState(
          {},
          null,
          this.$route.path + '#' + encodeURIComponent(params)
        )
      }
    },
    beforeMount(){
        this.getServers(null);
    },
    watch : {
      async'$route.query'(){
        this.servers = []
        await this.getServers(null)
      }
    }
}
</script>
<style scoped>
.container-list-holder{
  max-height: 80vh;
  overflow-y: auto;
}
.popup-holder{
  width: 100%;
  height: 100%;
}
.hoder-supervision{
  height: 100%;
  max-height: 100vh;
  width: 100%;

  display: grid;
  grid-template-rows: 120px  50px  1fr;
}
.Welcomeback{
  height: auto;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: start;

  gap : 5px;
  padding : var(--medieum-padding);
  box-sizing: border-box;
  border-radius: var(--medieum-border-radius);



  color:white;
}


</style>