<template>
    <createEditForm>

        <template #Header>
            <!-- Creating a new script -->
            <slot name="Header"></slot>
        </template>

        <template #formContent>
            <div class="input-name input-holder">
                <label>Name</label>
                <slot name="InputName" ></slot>
            </div>
            <div class="input-language input-holder">
                <label>Language</label>
                <slot name="InputLanguage" ></slot>
            </div>
            <div style="max-height: 115px;" class="description input-holder">
                <label>Description</label>
                <slot name="InputDescription" ></slot>
            </div>
            <div class="inputs input-holder" :class="{ 'forbidden' :forbiddenInput }">
                <div class="add-option">
                    <label>Inputs</label>
                    <slot name="InputAdd" ></slot>
                </div>
                <slot name="Inputs"></slot>
            </div>
            <div class="content">
                <slot name="CodeEditor"></slot>
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
    </createEditForm>
</template>
<script>


import createEditForm from "@/components/forms/incident-form.vue"

export default{
    name : 'create-server',
    components: {
        createEditForm,
    },
    props : 
        {forbiddenInput : Boolean}

}
</script>
<style scoped>
.buttons-footer{
    display: flex;
    justify-content: flex-end;

    gap: 10px;
    width: 50%;
}
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