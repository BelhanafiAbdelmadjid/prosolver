<template>

    <interractionLayout :forbiddenContainers="true" >

        <template #Header>
            {{ server.name + " server" }} 
        </template>
        <template #InputName>
            <input disabled type="text" placeholder="Server name..." v-model="server.name">
        </template>
        <template #InputIp>
            <input disabled type="text" placeholder="Server ip address..." v-model="server.ip">
        </template>
        <template #InputType>
            <select disabled v-model="server.type" name="" id="">
                <option value="UAT">UAT</option>
                <option value="PROD">Prod</option>
            </select>
        </template>
        <template #ContainerAddButton >
            <label style="cursor: pointer;">Add+</label>
        </template>
        <template #Containers>
            <tableExtension>
                <template #tableHeaders>
                    <td>Name</td>
                    <td>Added by</td>
                    <td>Actions</td>
                </template>
                <template #tableRows>
                    <tr v-for="container, index in server.containers" :key="index">
                        <td class="server-name">{{ container.name }}</td>
                        <td>
                            <p>{{ container.addedBy }}</p>
                        </td>
                        <td>
                            <p>Actions</p>
                        </td>
                    </tr>
                </template>
            </tableExtension>
        </template>
        <template v-if="this.AuthStore.userType == 'Admin'" #Footer>
            <buttonValidation :warning="true" @click="enterEditMode()"  :type="'submit'">
                <template #textButton>
                    Edit
                </template>
            </buttonValidation>
        </template>
        <template #popUps>

        </template>

    </interractionLayout>


</template>
<script>
import apiFetch from "@/common/api.service"

import interractionLayout from "./interraction-layout.vue"

import buttonValidation from "@/components/interraction/buttons/validation-button.vue"
import tableExtension from "@/components/interraction/tables/table-withextension.vue"

import { UseAuthStore } from "@/store/store"
export default{
    name : 'show-server',
    data(){
        return{
            server : {
                name : '' ,
                ip : '',
                type : "UAT" ,
                containers : [],
            },
            AuthStore : UseAuthStore()
        }
    },
    components: {
        buttonValidation,
        tableExtension,
        interractionLayout
    },
    methods : {
        createServer(){
            let endpoint = '/server/create';
            apiFetch.post(endpoint,
            {...this.server},
            true,
            false)
            .then(()=>{
                this.$router.push({name : 'serverShow' , params : { id : this.server.id}})
            })
        },
        enterEditMode(){
            if(this.AuthStore.userType == 'Admin'){
                this.$router.push({name : 'serverEdit' , props : { id : this.server.id } , query : { name : this.server.name, ip : this.server.ip, type : this.server.type }})
            }else{
                this.emitter.emit("sidebar-error",{
                    error : true,
                    description : "You are not allowed to enter edit mode please reach to an admin."
                })
            }
        }
    },
    created(){
        if(this.$route.query.name){
            this.server.name= this.$route.query.name
        }
        if(this.$route.query.type){
            this.server.type= this.$route.query.type
        }
        if(this.$route.query.ip){
            this.server.ip= this.$route.query.ip
        }

        let endpoint = "/server/"+this.$route.params.id;
        apiFetch.get(endpoint,false)
        .then((server)=>{
            this.server = server;
        })
    }
}
</script>
<style scoped>


.form-holder form{
    grid-template-columns: 1fr 1fr;


}
.form-holder form .input-name {
    grid-area: 1/1/2/2;
}
.form-holder form .input-name input, .form-holder form .input-type select{
    width: 100%;
}
.form-holder form .input-ip {
    grid-area: 2/1/3/3;
}
.form-holder form .input-type {
    grid-area: 1/2/2/3;
}
.form-holder .containers{

    grid-column: 1/3 ;
    grid-row: 3/5;

    height: 100%;
    width: 100%;
}

.add-option{
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.global-inputs{
    min-height: 50px;

    width: 100%;
    max-height: 100%;

    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;

    gap: 10px;

    overflow-x: auto;
}
.global-input{
    width: fit-content;
    background-color: white;

    display: grid;
    grid-template-columns: 1fr auto;
    grid-template-rows: 1fr 1fr ;

    gap: 10px;
}
.global-input input{
    width: 100%;

    grid-column : 1/3;
}
.global-input svg:hover{
    cursor: pointer;
}

.form-holder .table-containers{
    width: 100%;
    height: 100%;
}

</style>