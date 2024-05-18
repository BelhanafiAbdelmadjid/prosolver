<template>
    <div class="holders incidents-holder ">
        <queryNavbar @input-changed="onInputChanged" :theme="'flashy'" >
            <template #Title>
                Servers
            </template>
            <template #options>
                <p v-if="AuthStore.userType == 'Admin' " @click="$router.push({'name' : 'serverCreate'})" >create+</p>
            </template>
        </queryNavbar>
        <tableSimpleHeader v-if="loadingServers == false" >
            <template #tableHeaders >
                <td>Name</td>
                <td>IP</td>
                <td>Type</td>
                <td>Actions</td>
            </template>
            <template v-if="servers.length > 0"  #tableRows >
                <tr  v-for="server in servers" :key="server.id" >
                    <td>{{ server.name }}</td>
                    <td>{{ server.ip }}</td>
                    <td>{{ server.type }}</td>
                    <div class="user-actions" >
                        <div @click="goToServer(server)" class="user-action" >
                            <svg width="18" height="18" viewBox="0 0 512 512" fill="none" >
                                <path d="M384 224V408C384 413.253 382.965 418.454 380.955 423.307C378.945 428.16 375.999 432.57 372.284 436.284C368.57 439.999 364.16 442.945 359.307 444.955C354.454 446.965 349.253 448 344 448H104C93.3913 448 83.2172 443.786 75.7157 436.284C68.2143 428.783 64 418.609 64 408V168C64 157.391 68.2143 147.217 75.7157 139.716C83.2172 132.214 93.3913 128 104 128H271.48M336 64H448V176M224 288L440 72" stroke="#222222" stroke-width="32" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                            <p>Details</p>
                        </div>
                        <div v-if="AuthStore.userType == 'Admin'"  @click="deleteServer(server)" class="user-action" >
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M10 5H14C14 4.46957 13.7893 3.96086 13.4142 3.58579C13.0391 3.21071 12.5304 3 12 3C11.4696 3 10.9609 3.21071 10.5858 3.58579C10.2107 3.96086 10 4.46957 10 5ZM8.5 5C8.5 4.54037 8.59053 4.08525 8.76642 3.66061C8.94231 3.23597 9.20012 2.85013 9.52513 2.52513C9.85013 2.20012 10.236 1.94231 10.6606 1.76642C11.0852 1.59053 11.5404 1.5 12 1.5C12.4596 1.5 12.9148 1.59053 13.3394 1.76642C13.764 1.94231 14.1499 2.20012 14.4749 2.52513C14.7999 2.85013 15.0577 3.23597 15.2336 3.66061C15.4095 4.08525 15.5 4.54037 15.5 5H21.25C21.4489 5 21.6397 5.07902 21.7803 5.21967C21.921 5.36032 22 5.55109 22 5.75C22 5.94891 21.921 6.13968 21.7803 6.28033C21.6397 6.42098 21.4489 6.5 21.25 6.5H19.93L18.76 18.611C18.6703 19.539 18.238 20.4002 17.5477 21.0268C16.8573 21.6534 15.9583 22.0004 15.026 22H8.974C8.04186 22.0001 7.1431 21.653 6.45295 21.0265C5.7628 20.3999 5.33073 19.5388 5.241 18.611L4.07 6.5H2.75C2.55109 6.5 2.36032 6.42098 2.21967 6.28033C2.07902 6.13968 2 5.94891 2 5.75C2 5.55109 2.07902 5.36032 2.21967 5.21967C2.36032 5.07902 2.55109 5 2.75 5H8.5ZM10.5 9.75C10.5 9.55109 10.421 9.36032 10.2803 9.21967C10.1397 9.07902 9.94891 9 9.75 9C9.55109 9 9.36032 9.07902 9.21967 9.21967C9.07902 9.36032 9 9.55109 9 9.75V17.25C9 17.4489 9.07902 17.6397 9.21967 17.7803C9.36032 17.921 9.55109 18 9.75 18C9.94891 18 10.1397 17.921 10.2803 17.7803C10.421 17.6397 10.5 17.4489 10.5 17.25V9.75ZM14.25 9C14.0511 9 13.8603 9.07902 13.7197 9.21967C13.579 9.36032 13.5 9.55109 13.5 9.75V17.25C13.5 17.4489 13.579 17.6397 13.7197 17.7803C13.8603 17.921 14.0511 18 14.25 18C14.4489 18 14.6397 17.921 14.7803 17.7803C14.921 17.6397 15 17.4489 15 17.25V9.75C15 9.55109 14.921 9.36032 14.7803 9.21967C14.6397 9.07902 14.4489 9 14.25 9Z" fill="#E51D1D"/>
                            </svg>
                            <p>Delete</p>
                        </div>
                    </div>
                </tr>
            </template>
            
        </tableSimpleHeader>
        <tableSkeleton v-if="loadingServers == true" ></tableSkeleton>

    </div>
</template>
<script>
import apiFetch from "@/common/api.service.js"

import queryNavbar from "@/components/interraction/query/query-navbar.vue"
import tableSimpleHeader from "@/components/interraction/tables/table-normal-header.vue"

import tableSkeleton from "@/components/loadingAnimations/table-skeleton.vue"
import { UseAuthStore } from '@/store/store';

export default{
    name : 'incidents-index',
    data(){
        return{
            servers : [],
            loadingServers : true,
            AuthStore: UseAuthStore()
        }
    },
    components : {
        queryNavbar,
        tableSimpleHeader,
        tableSkeleton,
    },
    methods : {
        onInputChanged(input) {
            this.getservers(input);
        },
        getservers(query_name) {
            this.loadingServers = true;
            let endpoint = "/servers";
            if(query_name != null){
                endpoint = endpoint + "?name=" + query_name;
            }
            apiFetch.get(endpoint, false)
                .then((servers) => {
                    this.servers = servers;
                    if(query_name != null && servers.length == 0){
                        this.emitter.emit("sidebar-error",{error : true, description : "No server matching "+query_name+" was found."})
                    }
                    this.loadingServers = false;
                })

        },
        getServersWithNameLike(NameLike) {
            console.log(NameLike)
            //fetch here after
        },
        goToServer(server) {
            this.$router.push({ name: 'serverShow', params: { id: Number(server.id) }, query: { name: server.name, ip: server.ip, type: server.type } })
        },
        deleteServer(server){
            let endpoint = "/server/delete";
            apiFetch.delete(endpoint,
            {id : server.id},
            true,
            false)
            .then(()=>{
                this.$router.push("/servers");
                this.$router.go()
            })
        }
    },
    created(){
        this.getservers(null);
    }
}
</script>
<style scoped >
.incidents-holder{
    display: grid;
    grid-template-rows: auto 1fr;
    

    height: 100vh;
    
    width: 100%;
}
.user-actions{
    display: flex;
    justify-content: flex-start;
    align-items: center;

    gap: 25px;
    font-size: 13px;
    color: rgb(130, 130, 130);
    height: 50px;
}
.user-action{
    display: flex;
    justify-content: flex-start;
    align-items: center;

    gap: 2px;
}
.user-action:hover{
    cursor: pointer;
    border-bottom: solid 1px grey;
}

</style>