<template>
    <div :style="{'background-color' : colors[color] }" class="card" >
        <slot name="Type" ></slot>
    </div>
</template>
<script>
export default{
    data(){
        return{
            colors : {
                admin : '#d20606',
                worker : '#033032',
                viewer : '#249053',
                deactivated : 'gray'
            }
        }
    },

    props : {
        color : String
    }
}


</script>
<style>
.card{
    min-width: 50px;
    height: 20px;

    box-sizing: border-box;
    padding: 5px;

    border-radius: 15px;

    display: flex;
    justify-content: center;
    align-items: center;

    color: white;

    font-size: 12px;
}
</style>