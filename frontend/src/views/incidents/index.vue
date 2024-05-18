<template>
    <div class="incidents-holder holders ">
        <queryNavbar @input-changed="onInputChanged" :theme="'flashy'">
            <template #Title>
                Incidents
            </template>
            <template #options>
                <p v-if="AuthStore.userType == 'Admin' " @click="$router.push({'name' : 'incidentCreate'})">create+</p>
            </template>
        </queryNavbar>
        <div v-if="loadingIncidents == false && incidents.length != 0" class="cards">
            <cardRoute v-for="incident in incidents" :key="incident.id">
                <template #Titre>
                    {{ incident.name }}
                    <RouterLink v-if="AuthStore.userType == 'Admin'" style="display: flex;justify-content: center;align-items: flex-start;"
                        :to="{ name: 'incidentShow' , params : { id : incident.id } , query : {name : incident.name , description : incident.description} }">
                        <svg width="18" height="18" viewBox="0 0 512 512" fill="none">
                            <path
                                d="M384 224V408C384 413.253 382.965 418.454 380.955 423.307C378.945 428.16 375.999 432.57 372.284 436.284C368.57 439.999 364.16 442.945 359.307 444.955C354.454 446.965 349.253 448 344 448H104C93.3913 448 83.2172 443.786 75.7157 436.284C68.2143 428.783 64 418.609 64 408V168C64 157.391 68.2143 147.217 75.7157 139.716C83.2172 132.214 93.3913 128 104 128H271.48M336 64H448V176M224 288L440 72"
                                stroke="#222222" stroke-width="32" stroke-linecap="round" stroke-linejoin="round" />
                        </svg>
                    </RouterLink>
                </template>
                <template #icon>
                    <RouterLink
                        :to="{ name: 'incidentExecute' , params : { id : incident.id } , query : {name : incident.name , description : incident.description} }">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <g clip-path="url(#clip0_125_4)">
                                <path
                                    d="M12 2C12.2652 2 12.5196 2.10536 12.7071 2.29289C12.8946 2.48043 13 2.73478 13 3V3.055C15.0289 3.28241 16.9202 4.19257 18.3638 5.63618C19.8074 7.07978 20.7176 8.97114 20.945 11H21C21.2652 11 21.5196 11.1054 21.7071 11.2929C21.8946 11.4804 22 11.7348 22 12C22 12.2652 21.8946 12.5196 21.7071 12.7071C21.5196 12.8946 21.2652 13 21 13H20.945C20.7176 15.0289 19.8074 16.9202 18.3638 18.3638C16.9202 19.8074 15.0289 20.7176 13 20.945V21C13 21.2652 12.8946 21.5196 12.7071 21.7071C12.5196 21.8946 12.2652 22 12 22C11.7348 22 11.4804 21.8946 11.2929 21.7071C11.1054 21.5196 11 21.2652 11 21V20.945C8.97114 20.7176 7.07978 19.8074 5.63618 18.3638C4.19257 16.9202 3.28241 15.0289 3.055 13H3C2.73478 13 2.48043 12.8946 2.29289 12.7071C2.10536 12.5196 2 12.2652 2 12C2 11.7348 2.10536 11.4804 2.29289 11.2929C2.48043 11.1054 2.73478 11 3 11H3.055C3.28241 8.97114 4.19257 7.07978 5.63618 5.63618C7.07978 4.19257 8.97114 3.28241 11 3.055V3C11 2.73478 11.1054 2.48043 11.2929 2.29289C11.4804 2.10536 11.7348 2 12 2ZM13 5.07V6C12.9997 6.25488 12.9021 6.50003 12.7272 6.68537C12.5522 6.8707 12.313 6.98223 12.0586 6.99717C11.8042 7.01211 11.5536 6.92933 11.3582 6.76574C11.1627 6.60214 11.0371 6.3701 11.007 6.117L11 6V5.07C9.54779 5.28032 8.19827 5.94131 7.14184 6.9597C6.08541 7.97809 5.37541 9.30247 5.112 10.746L5.071 11H6C6.25488 11.0003 6.50003 11.0979 6.68537 11.2728C6.8707 11.4478 6.98223 11.687 6.99717 11.9414C7.01211 12.1958 6.92933 12.4464 6.76574 12.6418C6.60214 12.8373 6.3701 12.9629 6.117 12.993L6 13H5.07C5.28032 14.4522 5.94131 15.8017 6.9597 16.8582C7.97809 17.9146 9.30247 18.6246 10.746 18.888L11 18.929V18C11.0003 17.7451 11.0979 17.5 11.2728 17.3146C11.4478 17.1293 11.687 17.0178 11.9414 17.0028C12.1958 16.9879 12.4464 17.0707 12.6418 17.2343C12.8373 17.3979 12.9629 17.6299 12.993 17.883L13 18V18.93C14.4522 18.7197 15.8017 18.0587 16.8582 17.0403C17.9146 16.0219 18.6246 14.6975 18.888 13.254L18.929 13H18C17.7451 12.9997 17.5 12.9021 17.3146 12.7272C17.1293 12.5522 17.0178 12.313 17.0028 12.0586C16.9879 11.8042 17.0707 11.5536 17.2343 11.3582C17.3979 11.1627 17.6299 11.0371 17.883 11.007L18 11H18.93C18.7197 9.54779 18.0587 8.19827 17.0403 7.14184C16.0219 6.08541 14.6975 5.37541 13.254 5.112L13 5.07ZM12 10.5C12.3978 10.5 12.7794 10.658 13.0607 10.9393C13.342 11.2206 13.5 11.6022 13.5 12C13.5 12.3978 13.342 12.7794 13.0607 13.0607C12.7794 13.342 12.3978 13.5 12 13.5C11.6022 13.5 11.2206 13.342 10.9393 13.0607C10.658 12.7794 10.5 12.3978 10.5 12C10.5 11.6022 10.658 11.2206 10.9393 10.9393C11.2206 10.658 11.6022 10.5 12 10.5Z"
                                    fill="#9747FF" />
                            </g>
                            <defs>
                                <clipPath id="clip0_125_4">
                                    <rect width="24" height="24" fill="white" />
                                </clipPath>
                            </defs>
                        </svg>
                    </RouterLink>
                </template>

                <template #Description>
                    {{ incident.description }}
                </template>
            </cardRoute>
        </div>
        <div v-if="loadingIncidents == true" class="cards cards-loader" >
            <loadingCard style="width:100%;" ></loadingCard>
            <loadingCard style="width:100%"></loadingCard>
            <loadingCard style="width:100%"></loadingCard>
            <loadingCard style="width:100%"></loadingCard>
            <loadingCard style="width:100%"></loadingCard>
            <loadingCard style="width:100%"></loadingCard>
        </div>
        <div v-if="loadingIncidents == false && incidents.length == 0" class="cards cards-loader" >
            <p>No matching incident was found...</p>
        </div>
    </div>
</template>
<script>
import apiFetch from "@/common/api.service.js"

import queryNavbar from "@/components/interraction/query/query-navbar.vue"
import cardRoute from "@/components/interraction/cards/card-route.vue"

import loadingCard from "@/components/loadingAnimations/loading-card.vue"

import { UseAuthStore } from '@/store/store';

export default{
    name : 'incidents-index',
    data(){
        return{
            incidents : [],
            loadingIncidents : true,
            AuthStore : UseAuthStore()
        }
    },
    components : {
        queryNavbar,
        cardRoute,
        loadingCard
    },
    methods : {
        onInputChanged(query_name){
            this.getincidents(query_name);
        },
        getincidents(query_name){
            //fetch here
            this.loadingIncidents=true;
            let endpoint = "/incidents"
            if(query_name != null){
                endpoint = endpoint + "?name="+query_name;
            }
            apiFetch.get(endpoint,false)
            .then( (incidents)=>{
            this.incidents= incidents;
            if(query_name != null && incidents.length ==0){
                this.emitter.emit("sidebar-error",{error : true,description : "No incident matching "+query_name+" was found."})
            }
            this.loadingIncidents = false;
            })

        },
        getServersWithNameLike(NameLike){
            console.log(NameLike)
      },
    },
    created(){
        this.getincidents();
    }
}
</script>
<style scoped >
.cards-loader{
    overflow: hidden;
}
.incidents-holder{
    display: grid;
    grid-template-rows: auto 1fr;
    

    height: 100%;
    max-height: 100vh;
    width: 100%;
}
.cards{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: repeat(50px) ;
    grid-auto-rows: 125px;

    border-radius: 10px;

    overflow-y: auto;
    max-height: 100%;

}
.cards::-webkit-scrollbar {
  width: 4px; /* Width of the scrollbar */
}

/* Handle portion of the scrollbar */
.cards::-webkit-scrollbar-thumb {
  background-color: #999; /* Color of the thumb */
  border-radius: 4px; /* Border radius of the thumb */
}

/* Track (background) of the scrollbar */
.cards::-webkit-scrollbar-track {
  background-color: #f0f0f0; /* Color of the track */
}


@media only screen and (max-width: 1000px) {
    .incidents-holder{
        max-height: calc(100vh - 50px);
    }
}

</style>