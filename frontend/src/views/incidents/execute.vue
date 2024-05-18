<template>
    <div class="holders execution-holder">
        <div class="header colorfull-gradient-1">
            Executing incident
        </div>
        <div
            style="box-sizing:border-box; padding: 10px; background-color:rgb(240, 240, 240); border-radius: 10px; display:grid;grid-template-rows:auto; gap:10px;">
            <p>
                <strong>Global inputs </strong>
            </p>
            <div class="input-holders"
                style="padding:0px;display: flex;flex-direction: row;justify-content: flex-start;align-items :center; gap:5px;"
                v-for="npt,index in incident.inputs" :key="index">
                <label>{{ npt.label }}</label>
                <input :placeholder="npt.label" :type="npt.type" v-model="npt.value" required>
            </div>
        </div>
        <div class="steps">
            <lineComponent v-for="step in incident.steps" :key="step.id">

                <template #Header>{{'Step '+step.order + ": " +step.name }}</template>
                <template #content>
                    <form @submit.prevent="excuteStepButton(step)" >
                        <div class="step-left-side">
                            <div class="step-inputs">
                                <div v-for="input in step.inputs" :key="input.id" class="input-holder"
                                    style=" background-color: white; display: flex;flex-direction: column;justify-content: flex-start;align-items :flex-start; gap:5px;box-sizing: border-box;">
                                    <label for="type" >{{ input.label }}: </label>

                                    <input v-if="!input.fromIncident"   style="width: 100%;" :placeholder="input.label" :type="input.type" v-model="input.value" required >
                                    <input v-else @abort="console.log('test')"  :required="true"  :placeholder="input.label" style="width: 100%;" :type="input.type" v-model="lookForGlobalInput(input).value"  disabled >
                                </div>

                            </div>
                            <div class="step-footer colorfull-gradient-1">
                                <p>
                                    Executing <strong>{{" "+ step.script.name + ' ' }}</strong> on {{ (step.onServer ==
                                    true ? step.server.name : step.container.name + ' container of ' + step.server.name
                                    ) }}
                                </p>
                                <div class="shell-buttons">
                                    <buttonValidation style="width: 100%;padding:0;" :warning="true" :type="'Reset'">
                                        <template #textButton>
                                            Reset
                                        </template>
                                    </buttonValidation>
                                    <buttonValidation  style="width: 100%;padding:0;" :ok="true" :type="'Submit'">
                                        <template #textButton>
                                            Execute
                                        </template>
                                    </buttonValidation>

                                </div>
                            </div>
                        </div>
                    </form>
                    <div class="step-shell" style="background-color: black;">
                            <lineShell 
                            v-for="line,index in step.shell" :key="index"
                            :last="false"
                            :username="AuthStore.getUsername"
                            :server="step.server.name"
                            :command="line.command"
                            :result="line.result"
                            :notWaitingForOutPut="notWaitingForOutPut"
                            > </lineShell>
                            
                            <lineShell 
                            :last="true"
                            :username="AuthStore.getUsername"
                            :server="step.server.name"
                            :notWaitingForOutPut="notWaitingForOutPut"
                            :validCommands="['clear']"
                            @fill-shell="(cmd)=>{fillShell(cmd,step)}"
                            > </lineShell>
                    </div>
                </template>

            </lineComponent>
        </div>
    </div>
</template>

<script>
import apiFetch from "@/common/api.service.js"
import { UseAuthStore } from "@/store/store.js"

import lineComponent from "@/components/incident-execute/step-lines.vue"
import buttonValidation from "@/components/interraction/buttons/validation-button.vue"
import lineShell from "@/components/incident-execute/shellline.vue"

export default{
    name : 'incident-execute',
    data(){
        return {
            AuthStore : UseAuthStore(),
            incident: {

            },
            openBooleans : {},
            notWaitingForOutPut : true,
        }
    },
    methods : {
        lookForGlobalInput(input){
            let res = this.incident.inputs.find(item => item.id === input.parentInput);
            input.value = res.value;
            return res;
        },
        async fillShell(cmd,step){
            if (cmd == 'clear') {
                step.shell = [{ command: 'clear' }]
            } else if (cmd == 'exec' || cmd == 'execute') {
                await this.executeStep(step)
            } else {
                step.shell.push({
                    command: cmd,
                    result: [
                        {
                            value: "Command: '" + cmd + "' not found please contact your support.",
                            type: 'warning'
                        }
                    ]
                })
            }
        },
        async executeStep(step){
            if(this.notWaitingForOutPut != false){
                this.notWaitingForOutPut = false;
            let endpoint = '/incident/step/execute'
            await apiFetch.post(endpoint,{
                id : step.id,
                inputs : step.inputs,
            },true,true)
            .then((res)=>{
                console.log('result execution', res)
                let allRes = []
                if(res.warning){
                    for(let line of res.warning){
                        allRes.push({
                            value : line ,
                            type : 'warning'
                        })
                    }
                }
                if(res.error){
                    for(let line of res.error){
                        allRes.push({
                            value : line,
                            type : 'error'
                        })
                    }
                }
                if(res.result){
                    for(let line of res.result){
                        allRes.push({
                            value : line ,
                            type : 'correct'
                        })
                    }
                }

                step.shell.push({
                    command : 'execute',
                    result : [...allRes]
                })
                this.notWaitingForOutPut = true;
            })
            .catch(()=>{
                this.notWaitingForOutPut = true;
            })
            }else{
                this.emitter.emit("sidebar-error",{
                    error : true ,
                    description : 'Please wait, a step is already being executed.'
                })
            }

        },
        async excuteStepButton(step){
            await this.executeStep(step)
        }
    },
    components : {
        lineComponent,
        buttonValidation,
        lineShell
    },
    created(){
        let endpoint = "/incident/"+ this.$route.params.id ;
        apiFetch.get(endpoint,false,false)
        .then((incident)=>{
            this.incident = incident;
            for(let step of this.incident.steps){
                step.shell = [];
            }
            console.log(this.incident.steps)
        })
    }
}
</script>
<style scoped>
.execution-holder{
    width: 100%;

    display: grid;
    grid-template-rows: auto auto 1fr;

    
    height: 100vh;
    width: 100%;

    padding: var(--small-padding);
    box-sizing: border-box;

    overflow-y: auto;


}
.execution-holder .header{
    padding: 10px;
    box-sizing: border-box;

    font-size: 24px;
    font-weight: 700;

    color :white;
}
.execution-holder .steps{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;

    gap: 5px;

    overflow-y: auto;

    max-height: 100%;


}

.execution-holder .steps::-webkit-scrollbar {
  width: 4px; /* Width of the scrollbar */
}

/* Handle portion of the scrollbar */
.execution-holder .steps::-webkit-scrollbar-thumb {
  background-color: #999; /* Color of the thumb */
  border-radius: 4px; /* Border radius of the thumb */
}

/* Track (background) of the scrollbar */
.execution-holder .steps::-webkit-scrollbar-track {
  background-color: #f0f0f0; /* Color of the track */
}

.content form{
    height: 100%;
    width: 100%;

    display: grid;
    grid-template-columns: 1fr ;

    padding: var(--extra-small-padding);
    gap:var(--extra-small-padding);
    box-sizing: border-box;

}
.step-left-side{

    height: 100%;
    width: 100%;

    max-height: 100%;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;

}
.step-shell{
    height: 100%;
    width: 100%;
    max-width: 100%;
    overflow-x: auto;

    border-radius: var(--extra-small-border-radius);

    padding: var(--extra-small-padding);
    box-sizing: border-box;
}
.step-shell::-webkit-scrollbar {
  width: 4px; /* Width of the scrollbar */
}

/* Handle portion of the scrollbar */
.step-shell::-webkit-scrollbar-thumb {
  background-color: #999; /* Color of the thumb */
  border-radius: 4px; /* Border radius of the thumb */
}

/* Track (background) of the scrollbar */
.step-shell::-webkit-scrollbar-track {
  background-color: #f0f0f0; /* Color of the track */
}
.step-footer{
    height: 70px;
    width: 100%;

    color: var(--white-text-color );
    padding: var(--extra-small-padding);
    box-sizing: border-box;

    border-radius: var(--extra-small-border-radius);

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: space-between;

    font-size: 14px;
    text-align: left;

    gap: 5px;

    justify-self: flex-end;

}
.step-footer .shell-buttons{
    width: 100%;
    
    display: flex;
    justify-content: space-between;
    align-items: center;

    gap: 5px;

}

.step-inputs{

    font-size: 14px;

    height: 100%;
    width: 100%;

    max-height: 100%;
    overflow-y: auto;

    box-sizing: border-box;
}
.step-inputs::-webkit-scrollbar {
  width: 4px; /* Width of the scrollbar */
}

/* Handle portion of the scrollbar */
.step-inputs::-webkit-scrollbar-thumb {
  background-color: #999; /* Color of the thumb */
  border-radius: 4px; /* Border radius of the thumb */
}

/* Track (background) of the scrollbar */
.step-inputs::-webkit-scrollbar-track {
  background-color: #f0f0f0; /* Color of the track */
}


@media only screen and (max-width: 1000px) {

.execution-holder{
    height: calc(100vh - var(--navbar-thin-height));
}

}




</style>