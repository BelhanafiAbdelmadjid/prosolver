<template>
    <div class="holders form-holder">
        <div class="header colorfull-gradient-1">
            <slot name="Header"></slot>
        </div>
        <form>
            <slot name="formContent"></slot>
        </form>
        <div class="buttons">
            <slot name="Footer" ></slot>
        </div>
        <slot name="popUps"></slot>
    </div>

</template>
<script>
export default{
    name : 'create-edit-form',
}
</script>
<style >
.form-holder .header{
    padding: 10px;
    box-sizing: border-box;

    font-size: 24px;
    font-weight: 700;

    color :white;

}

.form-holder{
    
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    
    height: 100vh;
    width: 100%;

    padding: var(--small-padding);
    box-sizing: border-box;

    overflow-y: auto;
}
.form-holder form::-webkit-scrollbar {
    width: 5px; /* Set the width of the scrollbar */
}

.form-holder form::-webkit-scrollbar-thumb {
    background-color: #888; /* Color of the scrollbar thumb */
    border-radius: 5px; /* Border radius of the scrollbar thumb */
}

.form-holder form::-webkit-scrollbar-track {
    background-color: #f2f2f2; 
}
.form-holder form{
    background-color: white;

    width: 100%;
    height: 100%;
    max-height: 100%;

    display: grid;
    grid-template-rows: min-content min-content min-content  1fr ;
    /* grid-template-columns: 1fr 1fr; */
    
    gap:15px;

    padding: var(--small-padding);
    box-sizing: border-box;

    border-radius: var(--small-border-radius);

    overflow-y: auto;
}
.buttons{
    display: flex;
    justify-content: flex-end;
    align-items: center;

    width: 100%;
}
.buttons button{
    width: 50%;
}
.form-holder .forbidden{
    opacity: 0.5;
    cursor:not-allowed;
    pointer-events:all;
    user-select: none;
}

.form-holder .forbidden *{
    pointer-events: none;
}
@media only screen and (max-width: 1000px) {

.form-holder{
    height: calc(100vh - var(--navbar-thin-height));
}

}

@media only screen and (max-width: 725px) {
    .buttons button{
        width: 100%;
    }


}

</style>