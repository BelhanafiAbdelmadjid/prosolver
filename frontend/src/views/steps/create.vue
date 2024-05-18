<template>
    <interraction>
        <template #ScriptHeader >Creating new step</template>


        <template #InputName >
            <input v-model="step.name"  type="text">
        </template>
        <template #InputScript >
            <select v-model="step.script" >
                <option v-for="script in req.scripts" :key="script.id" :value="script.id">{{ script.name+'.'+script.language }}</option>
            </select>
        </template>
        <template #InputServer >
            <select v-model="step.server"  >
                <option v-for="server in req.servers" :key="server.id" :value="server.id">{{ server.name}}</option>
            </select>
        </template>
        <template #InputContainerChekbox >
            <input type="checkbox" v-model="selectContainer" name="" id="">
        </template>
        <template v-if="selectContainer" #InputContainer >
            <select v-model="step.container"  >
                <option v-for="container in containersSelect" :key="container.id" :value="container.id">{{ container.name}}</option>
            </select>
        </template>



        <template #GlobalInputListing >
            <div style="height: 100%;width: 100%;" >
                <div class="input-config-holder" v-for="input,index in step.inputs" :key="index" >
                    <div class="input-config-line"   v-if="input.fromIncident" >
                        <p>Make <strong> {{ input.label +' ' }}</strong> input global.</p>
                        <input type="checkbox" v-model="input.fromIncident">
                    </div>
                    <div class="input-config-line"  v-else >
                        <p>Local <strong> {{ input.label +' ' }} </strong> input.</p>
                    </div>
                    
                </div>
            </div>
        </template>
        <template #Footer >
            <buttonValidation style="width: 100%;"  @click="createStep()" :ok="true" :type="'submit'">
                <template #textButton>
                    Create
                </template>
            </buttonValidation>
        </template> 

        <template #popUps >
            
        </template>

    </interraction>
</template>
<script>
import apiFetch from "@/common/api.service"
import interraction from "./interraction-script.vue"
import buttonValidation from "@/components/interraction/buttons/validation-button.vue"
export default{
    name : 'script-create',
    components : {
        interraction,
        buttonValidation
    },
    data(){
        return{
            step : {
                name : '',
                server : null ,
                container : null,
                script : null,
                inputs : []
            },
            req : {
                scripts : [],
                servers : [],
            },
            selectContainer : false,
            containersSelect : []
        }
    },
    watch : {
        'step.server'(){
            let server = this.req.servers.filter( server => server.id === this.step.server );
            this.containersSelect =  server[0].containers;
        },
        selectContainer(newV,oldV){
            if(oldV == false && newV == true){
                if(this.step.server == null){
                    this.emitter.emit("sidebar-error",{error : true , description : 'Please select a server first.'})
                    this.selectContainer = false;
                }
            }else if(oldV == true && newV == false){
                this.containersSelect = [];
            }
        },
        'step.script'(){
            let endpoint = '/incident/'+this.$route.params.id+'/script/'+this.step.script+'/join'
            apiFetch.get(endpoint,false)
            .then((inputs)=>{
                this.step.inputs = inputs
            })
        }
    },
    beforeMount(){
        // incident/3/step/create
        let endpoint = '/incident/'+ this.$route.params.id+'/step/create'
        apiFetch.get(endpoint,false)
        .then((req)=>{
            this.req =req;
        })
    },
    methods : {
        createStep(){

            for(let input of this.step.inputs){
                if(input.fromIncident == true){
                    input.parentInput = input.incidentID;
                }
            }

            let endpoint = '/incident/step/create';
            apiFetch.post(endpoint,{
                incident : this.$route.params.id,
                server : this.step.server,
                script : this.step.script,
                container : this.step.container,
                name : this.step.name,
                inputs : this.step.inputs
            },
            true,
            false)
            .then((res)=>{

                console.log(res)
            })

        }
    }
}
</script>
<style scoped>
.input-config-holder{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;

    gap: 5px;
    box-sizing: border-box;

    overflow-y: auto;

    width: 100%;


}
.input-config-line{

    width: 100%;

    padding: var(--extra-small-padding);
    box-sizing: border-box;

    border: solid 1px black;
    border-radius: 3px;

    background-color: white;

    display: flex;
    justify-content: flex-start;
    align-items: center;

    gap:3px;

    margin-top: 5px;
}
.input-config-line:hover{
    border: solid 1px var(--warm-color-1);
}


</style>