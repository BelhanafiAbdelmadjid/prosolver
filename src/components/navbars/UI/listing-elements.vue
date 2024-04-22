<template>
    <div class="holder">
        <h3 class="header"  @click="rolled = !rolled">
            <slot name="header" ></slot>
        </h3>
        <Transition name="showListeNavigation">
            <ul class="liste-holder" v-if="rolled" >
                <slot name="list" ></slot>
            </ul>
        </Transition>
    </div>
</template>
<script>
export default{
    data(){
        return {
            rolled : true
        }
    },
    props : ["subTitle"],
    beforeMount(){
        if(this.subTitle){
            this.rolled = false;
        }
    }

}
</script>
<style >
/* we will explain what these classes do next! */
.showListeNavigation-enter-active,
.showListeNavigation-leave-active {
  transition: all 0.25s ease;
}

.showListeNavigation-enter-from,
.showListeNavigation-leave-to {
    opacity: 0;
}

.header{
    background-color: rgb(248, 248, 248);
    border-radius: 5px;
    box-sizing: border-box;
    padding: 2px;
    width : 100%;
    font-size:16px;

    cursor: pointer;

    text-decoration: none;
    
}
.holder{
    /* user-select: none; */

    display:flex;
    flex-direction: column;
    gap:5px;
    width : 100%;
}
.holder ul{
    list-style: none;
    display:flex;
    justify-content: flex-start;
    align-items: center;
}
.liste-holder{
    margin-left: 10px;
    padding-left : 10px;
    border-left : solid rgb(248, 248, 248) 1px;
    display:flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: start;

    gap : 5px;
}
.liste-holder  li:hover{
    background-color: #662d91;
    color : rgb(248, 248, 248);
}
.liste-holder  li{
    transition: all 0.15s;
    
    width : 100%;
    cursor: pointer;
    background-color: rgb(248, 248, 248);
    border-radius: 5px;
    padding : 3px;
    box-sizing: border-box;

    display:flex;
    justify-content: flex-start;
    align-items: center;

}
.liste-holder  li * {
    width:100%;
    height:100%;
}
.liste-holder  li a{
    text-decoration: none; 
    color: inherit;
}


</style>