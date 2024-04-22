<template>
    <div class="sidebar">
     <transition v-for="square , index  in squares" :key="index" name="slide">
         <squareDisplay :error="square.error" >
            <template #description >
              <p>{{ square.description }}</p>
            </template>
        </squareDisplay>
     </transition>
    </div>
 </template>
     
 <script>
 import squareDisplay from "./square-display.vue"
 export default {
       name: 'sideBar-error',
       components: {
        squareDisplay
       },
       data(){
         return{
             squares : [
                 // {error : true,
                 // description : 'this is a test'}
             ]
         }
       },
       mounted(){
         this.emitter.on("sidebar-error",(payload)=>{
            console.log('recv',payload)
            this.squares.push(payload);
         })
       }
     }
 </script>
     
 <style scoped>
 .slide-enter-active, .slide-leave-active {
   transition: all 0.5s;
 }
 .slide-enter, .slide-leave-to {
   transform: translateX(calc(100% + 10px)); /* Start offscreen to the right */
 }
 .sidebar{
  position : fixed;
  height : 100vh;
  width : 30vw;
  min-width: 200px;
  right :0;
  top : 0;
  pointer-events: none;

  display:grid;
  place-content: start;
  grid-gap : 10px;
  grid-template-columns: 1% 1fr 1%;
  padding: 10px;
  box-sizing : border-box;

  transition: 0.25s;
  z-index : 9999999999;
 }
 .sidebar *{
     grid-column: 2/3;
 }
     
 </style>