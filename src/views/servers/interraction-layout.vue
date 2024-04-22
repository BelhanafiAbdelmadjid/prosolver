<template>
    <createEditForm>

        <template #Header>
            <slot name="Header"></slot>
        </template>

        <template #formContent>
            <div class="input-name input-holder">
                <label>Name</label>
                <!-- <input type="text" placeholder="Server name..." v-model="server.name"> -->
                <slot name="InputName" ></slot>
            </div>
            <div class="input-ip input-holder">
                <label>IP address</label>
                <slot name="InputIp" ></slot>
            </div>
            <div style=" width: 100%" class="input-type input-holder">
                <label  >Type</label>
                <slot name="InputType" ></slot>
            </div>
            <div class="containers input-holder" :class="{ 'forbidden' : forbiddenContainers }" >
                
                <div class="add-option">
                    <label>Containers</label>
                    <slot name="ContainerAddButton"></slot>
                </div>
                <div class="table-containers">
                    <slot name="Containers" ></slot>
                </div>
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
    data(){
        return{
            server : {
                name : null ,
                ip : null,
                type : "UAT" ,
                containers : null,
            }
        }
    },
    components: {
        createEditForm,
    },
    props: {
    forbiddenContainers: Boolean,
  }
}
</script>

<style scoped>
.buttons-footer{
    width: 50%;

    gap: var(--extra-small-padding);
    padding: var(--extra-small-padding);
    box-sizing: border-box;
}

.form-holder form{
    grid-template-columns: 1fr 1fr ;
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
    position: relative;

    grid-column: 1/3 ;
    grid-row: 3/5;

    height: 100%;
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