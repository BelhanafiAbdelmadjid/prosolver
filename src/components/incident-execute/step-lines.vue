<template>
    <div @mouseenter="hovering = true" @mouseleave="hovering = false" class="line-holder"   >
        <div @click="opened = !opened;"  class="line-header" :class="{ 'line-header-opened' : hovering , 'colorfull-gradient-1' : hovering  , 'line-header-closed' : !hovering }" >
            <slot name="Header" ></slot>
        </div>
        <div v-show="opened == true" class="content">

            <slot name="content" ></slot>
        </div>
    </div>
</template>
<script>
export default{
    name : 'step-line',
    data() {
        return{
            hovering : false,
            opened : false
        }
    },
}
</script>
<style >

.line-header-opened{
    color:white;
    border: solid 1px white;

    border-top-left-radius: var(--extra-small-border-radius);
    border-top-right-radius: var(--extra-small-border-radius);

}
.line-header-closed{
    border: solid 1px black;

    border-top-left-radius: var(--extra-small-border-radius);
    border-top-right-radius: var(--extra-small-border-radius);

    border-bottom-left-radius: var(--extra-small-border-radius);
    border-bottom-right-radius: var(--extra-small-border-radius);
}

.line-header{


    display: flex;
    justify-content: flex-start;
    align-items: center;

    padding: var(--extra-small-padding);

    box-sizing: border-box;

    cursor: pointer;

    transition: all 0.15s ease-out;

}
.line-holder{
    width: 100%;
    border-radius: var(--extra-small-border-radius);
    box-sizing: border-box;
}
.line-holder-expend{
    overflow: visible;
}
.line-holder-closed{
    overflow: hidden;
}
.content{

    overflow: hidden;

    height: 50vh;

    background-color: var(--light-color-0);

    border-bottom-left-radius: var(--extra-small-border-radius);
    border-bottom-right-radius: var(--extra-small-border-radius);

    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}

</style>
    