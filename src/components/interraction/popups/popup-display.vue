<template>
    <div class="popup-holder">
        
        <div @click="closePopUp" class="layer">

        </div>
        
        <div class="popUp">
            <p class="popup-header"> <slot name="titel" ></slot> </p>
                <div class="pop-content-holder">
                    <slot name="content" ></slot>
                </div>
        </div>

    </div>
</template>
<script>
import {UseAuthStore} from '@/store/store'

  export default {
      name : "popup-display",
      components : {
      },
      data(){
        return{
            returnBox : {},
        }
      },
      methods : {
        closePopUp(){
            this.$emit("close-popup")
        },
        sendData(){
            this.$emit("close-popUp",this.returnBox);
        }
      },
      props : ["toFill","inputsSpecial"],
      mounted(){
  
      },
      setup(){
        const AuthStore = UseAuthStore();
        return{
          AuthStore,//permet de rendre le store accesible dans le tempalte
        }
      },
      watch : {
       
      }
  }
  </script>
<style scoped>
.pop-content-holder{
    width: 100%;
    height: 100%;

    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;

    gap:5px;
}
.popup-header{
    font-weight: 500;
    font-size: 20px;

    color : var(--gray-text-color-1 );
    border-bottom : solid 1px var(--gray-text-color-1 );

    width : 100%;
    align-self: center;

    padding : 3px;
    box-sizing: border-box;
    background-color : white;
   
}
.filingInputs{
    height : 100%;
    width : 100%;
    padding : 1%;
    box-sizing: border-box;
}
.popup-holder{
    position: absolute;
    top :0;
    left: 0;
    height : 100%;
    width : 100%;

    z-index: 9;
    /* background-color: red; */
}
.layer{
    position: absolute;
    top :0;
    left: 0;
    height : 100%;
    width : 100%;
    opacity: 0.75;
    background-color: rgb(233, 233, 233);

}
.popUp{
    position: absolute;
    top :50%;
    left: 50%;
    height : auto;
    transform: translateX(-50%) translateY(-50%);
    min-height: 10px;
    min-width : 50%;

    max-width: 100vw;
    max-height: 100vh;

    overflow: auto;

    background-color: rgb(248, 248, 248);
    gap:5px;
    
    display: flex;
    flex-direction : column ; 
    align-items: flex-start;
    justify-content: flex-start;

    box-sizing: border-box;
    padding: 10px;

    border-radius : 5px;

}
.popUp:nth-child(1){
    width: 100%;
}


.addButton{
    justify-content: flex-end;
    padding : 10px;
    box-sizing: border-box;
}
.addButton button{
    
    padding : 2px;
    box-sizing : border-box;
    border : none;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius : 5px;
    font-size : 14px;
    cursor : pointer;
    box-sizing : border-box;
    border : solid 1px #662d91;
}
.addButton button:hover{
    border : solid 1px #662d91;
}
</style>