<template>

    <interractionLayout :forbiddenContainers="false">

        <template #Header>
            {{ server.name + " server" }}
        </template>
        <template #InputName>
            <input type="text" placeholder="Server name..." v-model="server.name">
        </template>
        <template #InputIp>
            <input type="text" placeholder="Server ip address..." v-model="server.ip">
        </template>
        <template #InputType>
            <select v-model="server.type" name="" id="">
                <option value="UAT">UAT</option>
                <option value="PROD">Prod</option>
            </select>
        </template>
        <template #ContainerAddButton>
            <label @click="popUpBoolean=true;" style="cursor: pointer;">Add+</label>
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
                            <div @click="server.containers.splice(index,1)" class="user-action">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path
                                        d="M10 5H14C14 4.46957 13.7893 3.96086 13.4142 3.58579C13.0391 3.21071 12.5304 3 12 3C11.4696 3 10.9609 3.21071 10.5858 3.58579C10.2107 3.96086 10 4.46957 10 5ZM8.5 5C8.5 4.54037 8.59053 4.08525 8.76642 3.66061C8.94231 3.23597 9.20012 2.85013 9.52513 2.52513C9.85013 2.20012 10.236 1.94231 10.6606 1.76642C11.0852 1.59053 11.5404 1.5 12 1.5C12.4596 1.5 12.9148 1.59053 13.3394 1.76642C13.764 1.94231 14.1499 2.20012 14.4749 2.52513C14.7999 2.85013 15.0577 3.23597 15.2336 3.66061C15.4095 4.08525 15.5 4.54037 15.5 5H21.25C21.4489 5 21.6397 5.07902 21.7803 5.21967C21.921 5.36032 22 5.55109 22 5.75C22 5.94891 21.921 6.13968 21.7803 6.28033C21.6397 6.42098 21.4489 6.5 21.25 6.5H19.93L18.76 18.611C18.6703 19.539 18.238 20.4002 17.5477 21.0268C16.8573 21.6534 15.9583 22.0004 15.026 22H8.974C8.04186 22.0001 7.1431 21.653 6.45295 21.0265C5.7628 20.3999 5.33073 19.5388 5.241 18.611L4.07 6.5H2.75C2.55109 6.5 2.36032 6.42098 2.21967 6.28033C2.07902 6.13968 2 5.94891 2 5.75C2 5.55109 2.07902 5.36032 2.21967 5.21967C2.36032 5.07902 2.55109 5 2.75 5H8.5ZM10.5 9.75C10.5 9.55109 10.421 9.36032 10.2803 9.21967C10.1397 9.07902 9.94891 9 9.75 9C9.55109 9 9.36032 9.07902 9.21967 9.21967C9.07902 9.36032 9 9.55109 9 9.75V17.25C9 17.4489 9.07902 17.6397 9.21967 17.7803C9.36032 17.921 9.55109 18 9.75 18C9.94891 18 10.1397 17.921 10.2803 17.7803C10.421 17.6397 10.5 17.4489 10.5 17.25V9.75ZM14.25 9C14.0511 9 13.8603 9.07902 13.7197 9.21967C13.579 9.36032 13.5 9.55109 13.5 9.75V17.25C13.5 17.4489 13.579 17.6397 13.7197 17.7803C13.8603 17.921 14.0511 18 14.25 18C14.4489 18 14.6397 17.921 14.7803 17.7803C14.921 17.6397 15 17.4489 15 17.25V9.75C15 9.55109 14.921 9.36032 14.7803 9.21967C14.6397 9.07902 14.4489 9 14.25 9Z"
                                        fill="#E51D1D" />
                                </svg>
                                <p>Delete</p>
                            </div>
                        </td>
                    </tr>
                </template>
            </tableExtension>
        </template>
        <template #Footer>
            <buttonValidation @click="updateServer()" :ok="true" :type="'submit'">
                <template #textButton>
                    Save changes
                </template>
            </buttonValidation>
            <buttonValidation @click="$router.back()" :danger="true" :type="'submit'">
                <template #textButton>
                    Cancel
                </template>
            </buttonValidation>
        </template>
        <template #popUps>
            <popupDisplay v-if="popUpBoolean" @close-popup="popUpBoolean = false;">
                <template #titel>New container</template>
                <template #content>
                    <div class="input-holder"
                        style="display: flex;flex-direction: row;justify-content: flex-start;align-items :center; gap:5px;">
                        <label for="">Container name</label>
                        <input type="text" placeholder="Input label..." v-model="inputPopUP.name">
                    </div>
                    <buttonValidation :ok="true" @click="pushInput"
                        style=" padding: 2px;width: 50%;align-self: flex-end;">
                        <template #textButton>
                            Add
                        </template>
                    </buttonValidation>
                </template>
            </popupDisplay>
        </template>

    </interractionLayout>


</template>
<script>
import apiFetch from "@/common/api.service"
import { UseAuthStore } from "@/store/store.js"

import interractionLayout from "./interraction-layout.vue"

import buttonValidation from "@/components/interraction/buttons/validation-button.vue"
import popupDisplay from "@/components/interraction/popups/popup-display.vue"
import tableExtension from "@/components/interraction/tables/table-withextension.vue"
export default{
    name : 'show-server',
    data(){
        return{
            AuthStore : UseAuthStore(),
            server : {
                name : '' ,
                ip : '',
                type : "UAT" ,
                containers : [],
            },
            oldServer : {
                name : '' ,
                ip : '',
                type : "UAT" ,
                containers : [],
            },
            popUpBoolean : false,
            inputPopUP :  {
                    name : "",
                    id : null
                }
        }
    },
    components: {
        buttonValidation,
        tableExtension,
        interractionLayout,
        popupDisplay
    },
    methods : {
        updateServer(){
            this.keepUpdatedValue(this.oldServer,this.server,["id","containers"]);
            console.log("sending",this.server)

            let endpoint = '/server/edit';
            apiFetch.update(endpoint,
            {...this.server},
            true,
            false)
            .then(()=>{
                this.$router.push({name : 'serverShow' , params : { id : this.server.id}})
            })
        },
        keepUpdatedValue(oldObject, newObject, dontCheck) {
            for (const prop of Object.getOwnPropertyNames(oldObject)) {
                if (oldObject[prop] == newObject[prop] && !(dontCheck.includes(prop))) {
                    newObject[prop] = null;
                }
            }
        },
        addInput(){
            this.inputPopUP =  {
                    name : "",
                    id : null
                }
            this.popUpBoolean = true;
        },
        pushInput(){
            if(this.inputPopUP.name == ""  ){
                this.emitter.emit("sidebar-error",{
                    error : true , description : 'Please fill the required field.'
                })
                return ;
            }
            this.server.containers.push({...this.inputPopUP,addedBy : this.AuthStore.getUsername});
            this.popUpBoolean = false;
        },
    },
    created(){
        if(this.AuthStore.userType != 'Admin'){
            this.emitter.emit("sidebar-error",{error : true , description : "You are not allowed to edit scripts please reach to an admin."})
            this.$router.back()
        }
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
            this.oldServer =Object.assign({}, this.server); 
        })
    }
}
</script>
<style scoped>
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