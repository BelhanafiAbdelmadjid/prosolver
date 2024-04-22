<template>
    <interraction :forbiddenInputs="false" >
        <template #ScriptHeader >Edit step {{ step.name }}</template>


        <template #InputName >
            <input  v-model="step.name"  type="text">
        </template>
        <template #InputScript >
            <select  v-model="step.script" >
                <option v-for="script in req.scripts" :key="script.id" :value="script.id">{{ script.name+'.'+script.language }}</option>
            </select>
        </template>
        <template #InputServer >
            <select  v-model="step.server"  >
                <option v-for="server in req.servers" :key="server.id" :value="server.id">{{ server.name }}</option>
            </select>
        </template>
        <template #InputContainerChekbox >
            <input type="checkbox" v-model="selectContainer" name="" id="">
        </template>
        <template v-if="selectContainer" #InputContainer >
            <select  v-model="step.container"  >
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
            <buttonValidation   @click="updateStep()" :ok="true" :type="'submit'">
                <template #textButton>
                    Save changes
                </template>
            </buttonValidation>
            <buttonValidation   @click="$router.back()" :danger="true" :type="'submit'">
                <template #textButton>
                    Cancel
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
                server : {
                    id : null
                } ,
                container : {
                    id : null
                },
                script : {
                    id : null
                },
                inputs : []
            },
            oldStep :{},
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
            try{
                if(this.step.server){
                    let server = this.req.servers.filter( server => server.id === this.step.server );
                    this.containersSelect =  server[0].containers;
                    this.step.container = null;
                    if(this.containersSelect.length == 0 ){
                        this.selectContainer = false;
                    }
                }
            }catch{
                return;
            }
            
        },
        selectContainer(newV,oldV){
            if(oldV == false && newV == true){
                console.log("here is the selected server",this.step.server)
                if(this.step.server == null){
                    this.emitter.emit("sidebar-error",{error : true , description : 'Please select a server first.'})
                    this.selectContainer = false;
                }else if(this.step.container == null ){
                    this.containersSelect = this.req.servers.filter(server =>{ return server.id === this.step.server;})[0].containers;
                }
            }else if(oldV == true && newV == false){
                this.step.container = null;
                this.containersSelect = [];
            }
        },
        'step.script.id'(){
            if(this.script){
                let endpoint = '/incident/' + this.$route.params.id + '/script/' + this.step.script.id + '/join'
                apiFetch.get(endpoint, false)
                    .then((inputs) => {
                        this.step.inputs = inputs

                    })
            }
        }

    },
    created(){
        // incident/3/step/create

        let endpoint = '/incident/'+ this.$route.params.id+'/step/'+this.$route.params.stepID
        apiFetch.get(endpoint,false)
        .then((req)=>{
            console.log("step",req)
            this.step= req;
            this.step.server = this.step.server.id; 
            this.step.script = this.step.script.id; 
            if(this.step.container){
                this.selectContainer= true;
                this.step.container = this.step.container.id
            }
            this.oldStep =Object.assign({}, this.step); 
        })
        .then(()=>{
            let endpoint2 = '/incident/'+ this.$route.params.id+'/step/create'
            apiFetch.get(endpoint2, false)
            .then((req) => {
                this.req = req;
                console.log("req",this.req)
            })
            .then(()=>{
                console.log("this.step.container",this.step.container)
                    if (this.step.container) {
                        var containers = this.req.servers.filter(server => server.id === this.step.server);
                        this.containersSelect = containers[0].containers; // Fixed variable name here
                    }
            })
        })


    },
    methods : {
        updateStep(){
            let exclude = ["id","inputs","container"];
            
            this.keepUpdatedValue(this.oldStep,this.step,exclude);
            console.log("here is the step",this.step)
            let endpoint = '/incident/step/update';
            apiFetch.update(endpoint,{
                step : this.step.id,
                server : this.step.server,
                script : this.step.script,
                container : this.step.container,
                name : this.step.name,
                inputs : this.step.inputs,
                onServer : this.step.container == null ? true : false
            },
            true,
            false)
            .then(()=>{
                this.$router.back()
            })

        },
        keepUpdatedValue(oldObject, newObject, dontCheck) {
            for (const prop of Object.getOwnPropertyNames(oldObject)) {
                if (oldObject[prop] == newObject[prop] && !(dontCheck.includes(prop))) {
                    newObject[prop] = null;
                }
            }
        },
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