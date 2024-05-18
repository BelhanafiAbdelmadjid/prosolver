<template>
    <formTemplate>
        <template #Header>
            <slot name="ScriptHeader"></slot>
        </template>
        <template #formContent>
            <div class="input-name input-holder">
                <label>Step name</label>
                <slot name="InputName"></slot>
            </div>
            <div class="input-script input-holder">
                <label> Script</label>
                <slot name="InputScript"></slot>
            </div>
            <div class="input-server input-holder">
                <label>Server</label>
                <slot name="InputServer"></slot>
            </div>
            <div class="input-container input-holder">
                <label>Container <slot  name="InputContainerChekbox"></slot> </label>
                
                <slot  name="InputContainer"></slot>
            </div>

            <div class="input-holder  inputs-holder " :class="{ 'forbidden' : forbiddenInputs }"  >
                <div class="add-option">
                    <label>Inputs configuration</label>
                </div>
                <slot name="GlobalInputListing" ></slot>

            </div>

        </template>
        <template #Footer>
            <footer class="buttons-footer">
                <slot name="Footer" ></slot>
            </footer>

            
        </template>
        <template #popUps>
            <slot name="popUps" ></slot>

        </template>
    </formTemplate>
</template>
<script>
import formTemplate from "@/components/forms/incident-form.vue"
export default{
    name : 'step-interraction',
    components : {
        formTemplate
    },
    props : {
        forbiddenInputs : Boolean
    },
    data(){
        return {

        }
    }
}
</script>
<style >
.buttons-footer{
    width: 50%;

    gap: var(--extra-small-padding);
    padding: var(--extra-small-padding);
    box-sizing: border-box;

    display: flex;
    justify-content: flex-end;
    align-items: center;
}
.form-holder form{
    display: grid;

    grid-template-columns: 1fr ;
    grid-template-rows: min-content min-content min-content min-content  1fr ;
}
.inputs-holder{
    grid-row-start: 5 ;
    grid-row-end: 6;
    height: 100%;
    max-height: 100%;

    overflow-y: auto;
}
.input-holder select{
    width: 50%;
}
form-holder form .input-script{
    grid-row-start: 2 ;
    grid-row-end: 3;
}
form-holder form .input-server{
    grid-row-start: 3 ;
    grid-row-end: 4;
}
form-holder form .input-name{
    grid-row-start: 1 ;
    grid-row-end: 2;
}
form-holder form .input-container{
    grid-row-start: 4;
    grid-row-end: 5;
}

@media only screen and (max-width: 725px) {
    .input-holder select {
        width: 100%;
    }
}

</style>