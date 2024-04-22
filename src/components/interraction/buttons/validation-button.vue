<template>
    <button  :type="type" class="button" :class="{'ok' : ok , 'danger' : danger , 'warning-button' : warning }" > 
        <slot name="textButton">

        </slot>
    </button>
</template>
<script>
export default{
    name : 'validation-button',
    props : {
        type : String,
        ok : Boolean,
        danger : Boolean,
        warning : Boolean,
    }
}
</script>
<style scoped>
.button{
    cursor: pointer;
    font-size : 16px;
    
    
    border : none ;
    padding : 5px;
    box-sizing : border-box;

    border-radius: 5px;
    /* border : solid 1px black; */
    color : white;
    transition : all 0.25s;
}
.ok{
    background-color: #19c8a6;
}
.ok:hover{
    background-color: #00958e;
    opacity: 0.9;
}
.danger{
    background-color: var(--danger-color);
}
.danger:hover{
    opacity: 0.9;
    background-color: var(--danger-color-hover);
}
.warning-button{
    background-color: var(--warning-color);
}
.warning-button:hover{
    opacity: 0.9;
    background-color: var(--warning-color-hover);
}

</style>