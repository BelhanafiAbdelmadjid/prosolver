<template>

    <interrationLayout :forbiddenInput="true" >
        <template #Header>
            {{ script.name + ' script'}} 
        </template>
        <template #InputName>
            <input disabled type="text" placeholder="Script name..." v-model="script.name">
        </template>
        <template #InputLanguage>
            <select disabled  v-model="script.language">
                <option v-for="language,index in languages" :key="index" :value="language.value">{{language.value}}</option>
            </select>
        </template>
        <template #InputDescription>
            <textarea disabled maxlength="150" v-model="script.description"></textarea>
        </template>
        <template #InputAdd>
            <label @click="addInput()" style="cursor: pointer;">Add+</label>
        </template>
        <template #Inputs>
            <div v-if="script.inputs.length != 0" class="global-inputs">
                <globalInputCard v-for="globalInput, index in script.inputs" :key="index">
                    <template #inputs>
                        <select v-model="globalInput.type">
                            <option value="text">Text</option>
                            <option value="email">Email</option>
                            <option value="date">Date</option>
                            <option value="number">Number</option>
                        </select>
                        <svg @click="script.inputs.splice(index, 1)" width="20" height="20" viewBox="0 0 24 24"
                            fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M10 5H14C14 4.46957 13.7893 3.96086 13.4142 3.58579C13.0391 3.21071 12.5304 3 12 3C11.4696 3 10.9609 3.21071 10.5858 3.58579C10.2107 3.96086 10 4.46957 10 5ZM8.5 5C8.5 4.54037 8.59053 4.08525 8.76642 3.66061C8.94231 3.23597 9.20012 2.85013 9.52513 2.52513C9.85013 2.20012 10.236 1.94231 10.6606 1.76642C11.0852 1.59053 11.5404 1.5 12 1.5C12.4596 1.5 12.9148 1.59053 13.3394 1.76642C13.764 1.94231 14.1499 2.20012 14.4749 2.52513C14.7999 2.85013 15.0577 3.23597 15.2336 3.66061C15.4095 4.08525 15.5 4.54037 15.5 5H21.25C21.4489 5 21.6397 5.07902 21.7803 5.21967C21.921 5.36032 22 5.55109 22 5.75C22 5.94891 21.921 6.13968 21.7803 6.28033C21.6397 6.42098 21.4489 6.5 21.25 6.5H19.93L18.76 18.611C18.6703 19.539 18.238 20.4002 17.5477 21.0268C16.8573 21.6534 15.9583 22.0004 15.026 22H8.974C8.04186 22.0001 7.1431 21.653 6.45295 21.0265C5.7628 20.3999 5.33073 19.5388 5.241 18.611L4.07 6.5H2.75C2.55109 6.5 2.36032 6.42098 2.21967 6.28033C2.07902 6.13968 2 5.94891 2 5.75C2 5.55109 2.07902 5.36032 2.21967 5.21967C2.36032 5.07902 2.55109 5 2.75 5H8.5ZM10.5 9.75C10.5 9.55109 10.421 9.36032 10.2803 9.21967C10.1397 9.07902 9.94891 9 9.75 9C9.55109 9 9.36032 9.07902 9.21967 9.21967C9.07902 9.36032 9 9.55109 9 9.75V17.25C9 17.4489 9.07902 17.6397 9.21967 17.7803C9.36032 17.921 9.55109 18 9.75 18C9.94891 18 10.1397 17.921 10.2803 17.7803C10.421 17.6397 10.5 17.4489 10.5 17.25V9.75ZM14.25 9C14.0511 9 13.8603 9.07902 13.7197 9.21967C13.579 9.36032 13.5 9.55109 13.5 9.75V17.25C13.5 17.4489 13.579 17.6397 13.7197 17.7803C13.8603 17.921 14.0511 18 14.25 18C14.4489 18 14.6397 17.921 14.7803 17.7803C14.921 17.6397 15 17.4489 15 17.25V9.75C15 9.55109 14.921 9.36032 14.7803 9.21967C14.6397 9.07902 14.4489 9 14.25 9Z"
                                fill="#E51D1D" />
                        </svg>
                        <input type="text" placeholder="Input label..." v-model="globalInput.label">
                    </template>
                </globalInputCard>

            </div>
            <div v-else>
                <div class="warning">
                    <svg width="20" height="20" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="M19.064 3.80903C17.732 1.39903 14.268 1.39903 12.936 3.80903L2.44302 22.808C1.15502 25.14 2.84302 28 5.50702 28H26.494C29.158 28 30.846 25.14 29.557 22.808L19.064 3.80903ZM17.25 22C17.25 22.3315 17.1183 22.6495 16.8839 22.8839C16.6495 23.1183 16.3315 23.25 16 23.25C15.6685 23.25 15.3506 23.1183 15.1161 22.8839C14.8817 22.6495 14.75 22.3315 14.75 22C14.75 21.6685 14.8817 21.3506 15.1161 21.1161C15.3506 20.8817 15.6685 20.75 16 20.75C16.3315 20.75 16.6495 20.8817 16.8839 21.1161C17.1183 21.3506 17.25 21.6685 17.25 22ZM16 9.00003C16.2652 9.00003 16.5196 9.10538 16.7071 9.29292C16.8947 9.48046 17 9.73481 17 10V18C17 18.2652 16.8947 18.5196 16.7071 18.7071C16.5196 18.8947 16.2652 19 16 19C15.7348 19 15.4805 18.8947 15.2929 18.7071C15.1054 18.5196 15 18.2652 15 18V10C15 9.73481 15.1054 9.48046 15.2929 9.29292C15.4805 9.10538 15.7348 9.00003 16 9.00003Z"
                            fill="#FFD233" />
                    </svg>
                    <p class="warning-information">Your have no global inputs added yet.</p>
                </div>
            </div>
        </template>
        <template #CodeEditor>
            <CodeEditor v-model="script.content" :read-only="true" :line-nums="true" :header="true"
                :display-language="true" :copy-code="true" width="100%" max-width="100%" height="100%"
                :autofocus="false" theme="hybrid"></CodeEditor>
        </template>
        <template v-if="this.AuthStore.userType == 'Admin'" #Footer>
            <buttonValidation @click="enterEditMode()" :warning="true" :type="'submit'">
                <template #textButton>
                    Edit
                </template>
            </buttonValidation>
        </template>
        <template #popUps>

        </template>
    </interrationLayout>

</template>
<script>
import apiFetch from "@/common/api.service"

import CodeEditor from "simple-code-editor";

// import createEditForm from "@/components/forms/incident-form.vue"
import interrationLayout from "./interraction-layout.vue"
import buttonValidation from "@/components/interraction/buttons/validation-button.vue"
import globalInputCard from "@/components/interraction/cards/inputs-card.vue"

import { UseAuthStore } from "@/store/store";

export default{
    name : 'create-server',
    data(){
        return{
            AuthStore : UseAuthStore(),
            languages : [],
            script : {
                name : null ,
                language : null,
                content : "" ,
                inputs : [],
            },
            popUpBoolean : false,
            inputPopUP : {
                type : '',
                label : ''
            }
        }
    },
    components: {
        buttonValidation,
        CodeEditor,
        globalInputCard,
        interrationLayout
    },
    methods : {
        addInput(){
            this.inputPopUP =  {
                    label : "",
                    type : ""
                }
            this.popUpBoolean = true;
        },
        pushInput(){
            if(this.inputPopUP.label == "" || this.inputPopUP.type == ""  ){
                this.emitter.emit("sidebar-error",{
                    error : true , description : 'Please fill the required field.'
                })
                return ;
            }
            this.script.inputs.push({...this.inputPopUP});
            this.popUpBoolean = false;
        },
        createScript(){
            let endpoint = "/script/create";
            apiFetch.post(endpoint,
            {...this.script},
            true,
            false)
            .then((result)=>{
                this.$router.push({name : 'scriptShow' , params : { id : result.id }});
            })
        },
        enterEditMode(){
            if(this.AuthStore.userType == "Admin"){
                this.$router.push({name : 'scriptEdit' , params : {id : this.script.id} , query : {name : this.script.name , language : this.script.language , description : this.script.description}})
            }else{
                this.emitter.emit("sidebar-error",{
                    error : true,
                    description : "You are not allowed to enter edit mode please reach to an admin."
                })
            }
        }
    },
    created(){
        

        let endpoint = '/script/'+this.$route.params.id;
        apiFetch.get(endpoint,false)
        .then((script)=>{
            this.script = script;
        });
        let endpoint2 = '/languages'
        apiFetch.get(endpoint2,false)
        .then((languages)=>{
            this.languages = languages;
        });


    }
}
</script>
<style scoped>
.warning{
    width: 100%;
    border-radius: var( --extra-small-border-radius);

    display: flex;
    justify-content: flex-start;

    padding: var(--small-padding);
    box-sizing: border-box;

    gap: 5px;

    background-color: white;
}


.content{
    height: 400px;
    width: 100%;
    max-width: 100%;
    overflow-x: auto;

    grid-row: 5/6;

    background-color: none;
    color: black;
}
.form-holder form{
    grid-template-rows: auto;
    grid-template-columns: 1fr;

    overflow-y: auto;
}
.form-holder form .input-name input, .form-holder form .input-language select{
    width: 50%;
}
.form-holder form .input-name {
    grid-row: 1/2;
}
.form-holder form .input-language {
    grid-row: 2/3;
}
.form-holder .description{
    grid-row: 3/4;
}
.form-holder .inputs{
    grid-row: 4/5;
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
@media only screen and (max-width: 725px) {
    .form-holder form .input-name input,
        .form-holder form .input-language select {
            width: 100%;
        }
}


</style>