<template>
    <div class="lineShell">
        <p>
            <span class="user" >{{ username }}</span>
            <span>@</span>
            <span class="server">{{ server }}</span>
            <span v-if="cursor && filled == '' && last && notWaitingForOutPut"  :class="{'typing-cursor' : last}">:$ ~</span>
            <span v-else >:$ ~</span>
            <span  class="command" >{{ command }}</span>
            
            <input v-focus style="width: fit-content;"  v-if="last && notWaitingForOutPut"  @focusin="removeCursor"  @input="checkColor" @keydown.enter="Sending" class="typeInput " :class="{'yellow' : ok,'red' : !ok}"  v-model="filled">
        </p>
        <div class="result">
            <p @click="copyURL(res.value)" class="result-line" :class="{'result-error' : (res.type == 'error'),'result-correct' : (res.type == 'correct'),'result-warning' : (res.type == 'warning')}"  v-for="res,index in result" :key="index" >
                {{ res.value }}
            </p>
        </div>

    </div>
</template>
<script>
 export default {
     name : "lineShell-vue",
     components : {
      
     },
   
     data(){
        return {
            cursor : true,
            filled : "",
            ok : false,
            
            }
     },methods:{
        async copyURL(mytext) {
            if(navigator.clipboard){
             console.log(mytext)
             await navigator.clipboard.writeText(mytext)
             .then(()=>{
                this.emitter.emit("sidebar-error", {
                 error: false,
                 description: "Copied successfully."
             })
             })
            }else{
                this.emitter.emit("sidebar-error", {
                 error: true,
                 description: "Clip board API is not supported by your browser."
             })
                
            }

        },
        removeCursor(){
        this.cursor = false;
        },
        addCursor(){
        this.cursor = true;
        },
        checkColor(){
        for(let lineOk in this.validCommands ){
            if(this.validCommands[lineOk] == this.filled.trim()){
            return this.ok = true;
            }
        }
        return this.ok = false;

        },
        Sending(){
            this.$emit("fill-shell",(this.filled.trim()));
            this.filled = "";
        },
      
     },
     props : ["last","result","username","command","validCommands","server","notWaitingForOutPut"],
     mounted(){
     }
 }
</script>
<style scoped>
.result-line{
    cursor: pointer;
    transition: all 0.15s;
    
    width: 100%;


}
.result-line:hover{
    opacity: 0.6;
    background-color: white;
    color: black;

    padding: 3px;
    box-sizing: border-box;
}


.result-error{
  color: red;
}

.result-correct{
  color: green;
}
.result-warning{
    color : #ff9b04;
}
.result{
  width: 100%;

  box-sizing: border-box;
  padding-top : 5px;

  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
  
}
.yellow{
  color : yellow;
}
.red{
  color : red;
}
.typeInput{
    border: none;
    outline: none;
    padding: 0;
    margin: 0;
    background-color: transparent;

    /* pointer-events: all; */
    
}
.typing-cursor {
    position : relative;
}

/* Define the CSS animation keyframes */
@keyframes blinkCursor {
  0% ,100% {
    background-color: white;
  }
  50% {
    background-color: transparent;
  }

}

/* Apply the animation to the cursor bar when waiting for typing */
.typing-cursor::after {
    animation: blinkCursor 0.75s infinite;
    position : absolute;
    content: "";
    display: inline-block;
    width: 1px;
    height: 14px;
    right : -4px ;
    
}

.input-container input {
  border: 2px solid #333;
  padding: 5px 10px;
  font-size: 16px;
  width: 300px;
  outline: none; /* Remove default focus outline */
}

@keyframes blink {
  0% {
    border-color: #333;
  }
  50% {
    border-color: transparent;
  }
  100% {
    border-color: #333;
  }
}

.input-container input:last-child::after {
  content: "";
  display: inline-block;
  width: 2px;
  height: 18px;
  background-color: #333;
  animation: blink 1s infinite;
}
.command{
    margin-left : 5px;
}
.lineShell{
    width: 100%;
    color : white;
    height: auto;
}
.user{
    color : #CA3EFB;
}
.server{
    color : #EBFF04;
}
.lineShell p{
    font-size : 13px;
    display: flex;
    flex-direction: row;
    flex-flow: wrap;
}
</style>  