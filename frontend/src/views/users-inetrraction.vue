<template>
    <div class="holders users-holder">
        <queryComponentVue @input-changed="onInputChanged" :theme="'flashy'">
            <template #Title>
                Users
            </template>
            <template #options>
                <p v-if="AuthStore.userType == 'Admin' " @click="viewPupUp = true">create+</p>
            </template>
        </queryComponentVue>

        <div v-if="loadingusers == false" class="table">
            <table>
                <tr>
                    <td>Username</td>
                    <td>User Role</td>
                    <td>Actions</td>
                </tr>
                <tr v-for="user in users" :key="user.id">
                    <td class="username">{{ user.username }}</td>
                    <td>
                        <div class="user-roles">
                            <usersRoleRect v-if="user.admin" :color="'admin'">
                                <template #Type>Admin</template>
                            </usersRoleRect>

                            <usersRoleRect v-else-if="user.execute" :color="'worker'">
                                <template #Type>Worker</template>
                            </usersRoleRect>

                            <usersRoleRect v-else-if="user.active" :color="'viewer'">
                                <template #Type>Viewer</template>
                            </usersRoleRect>

                            <usersRoleRect v-else :color="'deactivated'">
                                <template #Type>Deactivated</template>
                            </usersRoleRect>

                        </div>
                    </td>
                    <td>
                        <div v-if="user.active" class="user-actions">
                            <div @click="openPopUpForEdit(user)" class="user-action">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path opacity="0.5" fill-rule="evenodd" clip-rule="evenodd"
                                        d="M14.279 2.152C13.909 2 13.439 2 12.5 2C11.561 2 11.092 2 10.721 2.152C10.2285 2.35421 9.83639 2.74377 9.63101 3.235C9.53701 3.458 9.50101 3.719 9.48601 4.098C9.47934 4.3726 9.40274 4.64097 9.26346 4.87772C9.12417 5.11447 8.9268 5.31178 8.69001 5.451C8.44875 5.5851 8.17755 5.65615 7.90154 5.65754C7.62552 5.65894 7.35361 5.59065 7.11101 5.459C6.77301 5.281 6.52801 5.183 6.28601 5.151C5.75656 5.08148 5.22108 5.2238 4.79601 5.547C4.47801 5.789 4.24301 6.193 3.77401 7C3.30401 7.807 3.07001 8.21 3.01701 8.605C2.94701 9.131 3.09101 9.663 3.41701 10.084C3.56501 10.276 3.77401 10.437 4.09701 10.639C4.57401 10.936 4.88001 11.442 4.88001 12C4.88001 12.558 4.57401 13.064 4.09801 13.36C3.77401 13.563 3.56501 13.724 3.41601 13.916C3.25509 14.1239 3.13698 14.3617 3.06849 14.6156C3.00001 14.8694 2.98251 15.1343 3.01701 15.395C3.07001 15.789 3.30401 16.193 3.77401 17C4.24401 17.807 4.47801 18.21 4.79601 18.453C5.22001 18.776 5.75601 18.918 6.28601 18.849C6.52801 18.817 6.77301 18.719 7.11101 18.541C7.35374 18.4092 7.62583 18.3408 7.90204 18.3422C8.17825 18.3436 8.44963 18.4147 8.69101 18.549C9.17701 18.829 9.46501 19.344 9.48601 19.902C9.50101 20.282 9.53701 20.542 9.63101 20.765C9.83501 21.255 10.227 21.645 10.721 21.848C11.091 22 11.561 22 12.5 22C13.439 22 13.909 22 14.279 21.848C14.7716 21.6458 15.1636 21.2562 15.369 20.765C15.463 20.542 15.499 20.282 15.514 19.902C15.534 19.344 15.823 18.828 16.31 18.549C16.5513 18.4149 16.8225 18.3439 17.0985 18.3425C17.3745 18.3411 17.6464 18.4093 17.889 18.541C18.227 18.719 18.472 18.817 18.714 18.849C19.244 18.919 19.78 18.776 20.204 18.453C20.522 18.211 20.757 17.807 21.226 17C21.696 16.193 21.93 15.79 21.983 15.395C22.0174 15.1343 21.9997 14.8693 21.9311 14.6155C21.8624 14.3616 21.7441 14.1239 21.583 13.916C21.435 13.724 21.226 13.563 20.903 13.361C20.426 13.064 20.12 12.558 20.12 12C20.12 11.442 20.426 10.936 20.902 10.64C21.226 10.437 21.435 10.276 21.584 10.084C21.7449 9.87606 21.863 9.63829 21.9315 9.38443C22 9.13057 22.0175 8.86566 21.983 8.605C21.93 8.211 21.696 7.807 21.226 7C20.756 6.193 20.522 5.79 20.204 5.547C19.7789 5.2238 19.2435 5.08148 18.714 5.151C18.472 5.183 18.227 5.281 17.889 5.459C17.6463 5.59083 17.3742 5.65922 17.098 5.65782C16.8218 5.65642 16.5504 5.58528 16.309 5.451C16.0724 5.31166 15.8752 5.11429 15.7361 4.87755C15.597 4.64081 15.5206 4.37251 15.514 4.098C15.499 3.718 15.463 3.458 15.369 3.235C15.2674 2.99174 15.1188 2.77088 14.9318 2.58506C14.7447 2.39923 14.5229 2.25208 14.279 2.152Z"
                                        fill="black" />
                                    <path
                                        d="M15.523 12C15.523 13.657 14.169 15 12.5 15C10.83 15 9.47699 13.657 9.47699 12C9.47699 10.343 10.83 9 12.5 9C14.17 9 15.523 10.343 15.523 12Z"
                                        fill="black" />
                                </svg>
                                <p>Modify roles</p>
                            </div>
                            <div @click="deleteUser(user)" class="user-action">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path
                                        d="M10 5H14C14 4.46957 13.7893 3.96086 13.4142 3.58579C13.0391 3.21071 12.5304 3 12 3C11.4696 3 10.9609 3.21071 10.5858 3.58579C10.2107 3.96086 10 4.46957 10 5ZM8.5 5C8.5 4.54037 8.59053 4.08525 8.76642 3.66061C8.94231 3.23597 9.20012 2.85013 9.52513 2.52513C9.85013 2.20012 10.236 1.94231 10.6606 1.76642C11.0852 1.59053 11.5404 1.5 12 1.5C12.4596 1.5 12.9148 1.59053 13.3394 1.76642C13.764 1.94231 14.1499 2.20012 14.4749 2.52513C14.7999 2.85013 15.0577 3.23597 15.2336 3.66061C15.4095 4.08525 15.5 4.54037 15.5 5H21.25C21.4489 5 21.6397 5.07902 21.7803 5.21967C21.921 5.36032 22 5.55109 22 5.75C22 5.94891 21.921 6.13968 21.7803 6.28033C21.6397 6.42098 21.4489 6.5 21.25 6.5H19.93L18.76 18.611C18.6703 19.539 18.238 20.4002 17.5477 21.0268C16.8573 21.6534 15.9583 22.0004 15.026 22H8.974C8.04186 22.0001 7.1431 21.653 6.45295 21.0265C5.7628 20.3999 5.33073 19.5388 5.241 18.611L4.07 6.5H2.75C2.55109 6.5 2.36032 6.42098 2.21967 6.28033C2.07902 6.13968 2 5.94891 2 5.75C2 5.55109 2.07902 5.36032 2.21967 5.21967C2.36032 5.07902 2.55109 5 2.75 5H8.5ZM10.5 9.75C10.5 9.55109 10.421 9.36032 10.2803 9.21967C10.1397 9.07902 9.94891 9 9.75 9C9.55109 9 9.36032 9.07902 9.21967 9.21967C9.07902 9.36032 9 9.55109 9 9.75V17.25C9 17.4489 9.07902 17.6397 9.21967 17.7803C9.36032 17.921 9.55109 18 9.75 18C9.94891 18 10.1397 17.921 10.2803 17.7803C10.421 17.6397 10.5 17.4489 10.5 17.25V9.75ZM14.25 9C14.0511 9 13.8603 9.07902 13.7197 9.21967C13.579 9.36032 13.5 9.55109 13.5 9.75V17.25C13.5 17.4489 13.579 17.6397 13.7197 17.7803C13.8603 17.921 14.0511 18 14.25 18C14.4489 18 14.6397 17.921 14.7803 17.7803C14.921 17.6397 15 17.4489 15 17.25V9.75C15 9.55109 14.921 9.36032 14.7803 9.21967C14.6397 9.07902 14.4489 9 14.25 9Z"
                                        fill="#E51D1D" />
                                </svg>
                                <p>Disable user</p>
                            </div>
                        </div>
                        <div v-else class="user-actions">
                            <div @click="reactivateUser(user)" class="user-action">
                                <svg width="16" height="16" viewBox="0 0 20 20" fill="none"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path
                                        d="M10 20C8.61667 20 7.31667 19.7373 6.1 19.212C4.88333 18.6867 3.825 17.9743 2.925 17.075C2.025 16.175 1.31267 15.1167 0.788 13.9C0.263333 12.6833 0.000666667 11.3833 0 10C0 8.13333 0.471 6.41233 1.413 4.837C2.355 3.26167 3.634 2.041 5.25 1.175C5.5 1.04167 5.76267 1.025 6.038 1.125C6.31333 1.225 6.509 1.40833 6.625 1.675C6.725 1.925 6.725 2.17933 6.625 2.438C6.525 2.69667 6.35833 2.89233 6.125 3.025C4.875 3.725 3.875 4.696 3.125 5.938C2.375 7.18 2 8.534 2 10C2 12.2333 2.775 14.125 4.325 15.675C5.875 17.225 7.76667 18 10 18C12.2333 18 14.125 17.225 15.675 15.675C17.225 14.125 18 12.2333 18 10C18 8.53333 17.625 7.17933 16.875 5.938C16.125 4.69667 15.125 3.72567 13.875 3.025C13.6417 2.89167 13.475 2.696 13.375 2.438C13.275 2.18 13.275 1.92567 13.375 1.675C13.475 1.40833 13.6543 1.21667 13.913 1.1C14.1717 0.983333 14.4173 0.991667 14.65 1.125C16.2833 1.975 17.5833 3.19167 18.55 4.775C19.5167 6.35833 20 8.1 20 10C20 11.3833 19.7373 12.6833 19.212 13.9C18.6867 15.1167 17.9743 16.175 17.075 17.075C16.175 17.975 15.1167 18.6877 13.9 19.213C12.6833 19.7383 11.3833 20.0007 10 20ZM9 10.175V1C9 0.716667 9.096 0.479333 9.288 0.288C9.48 0.0966668 9.71733 0.000666667 10 0C10.2833 0 10.521 0.0960001 10.713 0.288C10.905 0.48 11.0007 0.717333 11 1V10.175L12.9 8.3C13.0833 8.11667 13.3127 8.02067 13.588 8.012C13.8633 8.00333 14.1007 8.09933 14.3 8.3C14.4833 8.48333 14.575 8.71667 14.575 9C14.575 9.28333 14.4833 9.51667 14.3 9.7L10.7 13.3C10.5 13.5 10.2667 13.6 10 13.6C9.73333 13.6 9.5 13.5 9.3 13.3L5.7 9.7C5.51667 9.51667 5.42067 9.28767 5.412 9.013C5.40333 8.73833 5.49933 8.50067 5.7 8.3C5.88333 8.11667 6.11667 8.025 6.4 8.025C6.68333 8.025 6.91667 8.11667 7.1 8.3L9 10.175Z"
                                        fill="#0FA958" />
                                </svg>
                                <p>Reactivate user</p>
                            </div>

                        </div>
                    </td>
                </tr>

            </table>
        </div>
        <tableSkeleton v-if="loadingusers == true" ></tableSkeleton>

        <popUpAdd v-if="viewPupUpForUpdate" @close-popup="viewPupUpForUpdate = false;">
            <template #titel>Updating user role</template>
            <template #content>
                <div class="input-holder" style="display: flex;flex-direction: row;justify-content: flex-start;align-items :center; gap:5px;" >
                    <label style="font-weight:600;display: flex; gap:5px;">
                        Username
                        <usersRoleRect v-if="newUserType=='Admin'" :color="'admin'">
                            <template #Type>Admin</template>
                        </usersRoleRect>
                        <usersRoleRect v-else-if="newUserType=='Worker'" :color="'worker'">
                            <template #Type>Worker</template>
                        </usersRoleRect>
                        <usersRoleRect v-else-if="newUserType=='Viewer'" :color="'viewer'">
                            <template #Type>Viewer</template>
                        </usersRoleRect>
                    </label>
                    <input placeholder="Name..." v-model="newUser.username" type="text">
                </div>
                <div class="input-holder" style="display: flex;flex-direction: row;justify-content: flex-start;align-items :center; gap:5px;" >
                    <label style="font-weight:600;display: flex;">Role</label>
                    <select v-model="newUserType">
                        <option value="Admin">Admin</option>
                        <option value="Worker">Worker</option>
                        <option value="Viewer">Viewer</option>
                    </select>

                </div>
                <buttonValidation :ok="true" @click="update" style=" padding: 2px;width: 50%;align-self: flex-end;">
                    <template #textButton>
                        Update
                    </template>
                </buttonValidation>
            </template>
        </popUpAdd>
        <popUpAdd v-if="viewPupUp" @close-popup="viewPupUp = false;">

            <template #titel>Adding a new user</template>
            <template #content>
                <div class="input-holder"  style="display: flex;flex-direction: row;justify-content: flex-start;align-items :center; gap:5px;">
                    <label style="font-weight:600;display: flex; gap:5px;">
                        Username
                        <usersRoleRect v-if="newUserType == 'Admin'" :color="'admin'">
                            <template #Type>Admin</template>
                        </usersRoleRect>
                        <usersRoleRect v-else-if="newUserType == 'Worker'" :color="'worker'">
                            <template #Type>Worker</template>
                        </usersRoleRect>
                        <usersRoleRect v-else-if="newUserType == 'Viewer'" :color="'viewer'">
                            <template #Type>Viewer</template>
                        </usersRoleRect>
                    </label>
                    <input placeholder="Name..." v-model="newUser.username" type="text">
                </div>
                <div class="input-holder"  style="display: flex;flex-direction: row;justify-content: flex-start;align-items :center; gap:5px;">
                    <label style="font-weight:600;display: flex;">Role</label>
                    <select v-model="newUserType">
                        <option value="Admin">Admin</option>
                        <option value="Worker">Worker</option>
                        <option value="Viewer">Viewer</option>
                    </select>

                </div>

                <buttonValidation :ok="true" @click="createUser()"
                    style=" padding: 2px;width: 50%;align-self: flex-end;">
                    <template #textButton>
                        Add
                    </template>
                </buttonValidation>
            </template>

        </popUpAdd>
    </div>
</template>

<script>
import { UseAuthStore } from "@/store/store"
import apiFetch from "@/common/api.service.js"

import buttonValidation from "@/components/interraction/buttons/validation-button.vue"
import queryComponentVue from "@/components/interraction/query/query-navbar.vue"
import usersRoleRect from '@/components/users/role-select.vue'
import popUpAdd from "@/components/interraction/popups/popup-display.vue"
import tableSkeleton from "@/components/loadingAnimations/table-skeleton.vue"
export default{
    components : {
        queryComponentVue,
        usersRoleRect,
        buttonValidation,
        popUpAdd,
        tableSkeleton
    },
    data(){
        return {
            AuthStore : UseAuthStore(),
            users : [],

            viewPupUp: false,
            newUser : {},
            newUserType : "",
            
            viewPupUpForUpdate: false,
            loadingusers : true,

        }
    },
    watch : {

    },
    methods : {
        async createUser(){
            if(this.newUserType == "" || this.newUser.username == null || this.newUser.username == ""){
                this.emitter.emit("sidebar-error",{
                    error : true,
                    description : "Please fill the informations correctly."
                })
            return ;
            }
            switch(this.newUserType){
                case "Admin":
                    this.newUser.admin = true;
                    this.newUser.execute = true;
                    break;
                case "Worker":
                    this.newUser.admin = false;
                    this.newUser.execute = true;
                    break;
                default:
                    this.newUser.admin = false;
                    this.newUser.execute = false;
                    break;
            }
            let endpoint = "/user/create"
            apiFetch.post(endpoint,{...this.newUser},true,false)
             .then(()=>{
               this.$router.go();
            })
        },
        async deleteUser(user){
            let endpoint = '/user/delete';
            apiFetch.delete(endpoint,{id : user.id},true,false)
            .then(()=>{
                user.active = false;
            })
        },
        async reactivateUser(user){
            let endpoint = "/user/activate";
            apiFetch.update(endpoint,{id : user.id},true,false)
            .then(()=>{
                user.active = true;
            })
        },
        openPopUpForEdit(user){
            this.newUser.admin = user.admin;
            this.newUser.id = user.id;
            this.newUser.execute = user.execute;
            this.newUser.active = user.active;
            this.newUser.username = user.username;
            this.viewPupUpForUpdate = true;

            if(this.newUser.admin){
                this.newUserType = 'Admin';
            }else if(this.newUser.execute){
                this.newUserType = 'Worker';
            }else{
                this.newUserType = 'Viewer';
            }
        },
        async update(){

            if(this.newUserType == "" || this.newUser.username == null || this.newUser.username == ""){
                this.emitter.emit("sidebar-error",{
                    error : true,
                    description : "Please fill the informations correctly."
                })
                return ;
            }
            switch(this.newUserType){
                case "Admin":
                    this.newUser.admin = true;
                    this.newUser.execute = true;
                    break;
                case "Worker":
                    this.newUser.admin = false;
                    this.newUser.execute = true;
                    break;
                default:
                    this.newUser.admin = false;
                    this.newUser.execute = false;
                    break;
            }
            let endpoint = "/user/update"
            apiFetch.update(endpoint,{...this.newUser},true,false)
            .then(async ()=>{
                await this.getUsers()
                this.newUser = {};
                this.newUserType = "";
                this.viewPupUpForUpdate = false;
            })
        },
        getUsers(query_user){
            this.loadingusers=true;
            let endpoint = "/users";
            if(query_user != null){
                endpoint = endpoint + "?user="+query_user
            }
            apiFetch.get(endpoint,true)
            .then( (users)=>{
            this.users = users;
            if(query_user != null && users.length == 0){
                this.emitter.emit("sidebar-error",{error : true, description : "No user matching "+query_user+" was found."})
            }
            this.loadingusers= false;
            })
        },
        onInputChanged(input){
            this.getUsers(input);
        }
       
    },
    created(){
        this.getUsers()
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
.user-actions{
    display: flex;
    justify-content: flex-start;
    align-items: center;

    gap: 25px;
    font-size: 13px;
    color: rgb(130, 130, 130);
}
.user-roles{

    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 3px;
    height: 100%;
}
.username{
    font-weight: 500;
}
.users-holder{
    height : 100vh;
    width : 100%;

    display : grid;
    grid-template-rows : auto 1fr ;
    grid-template-columns : auto;

    padding : 10px;
    box-sizing : border-box;
}
.table table{
    width: 100%;
    background-color: white;
    border-radius: 5px;

    border-collapse: collapse;
}
.table table thead tr{
    height: 50px;
}
tr {
  border-bottom: 1px solid #ddd;
  height: 60px;
  width: 100%;
}
tr:hover {
    background-color: rgb(228, 228, 228);
}
tr td{
    padding: 5px;
    box-sizing: border-box;
}

</style>