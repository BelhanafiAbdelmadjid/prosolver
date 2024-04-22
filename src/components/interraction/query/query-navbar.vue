<template>
    <div :class="{ flashy : theme=='flashy' , white : theme == 'white'  }"  class="holder-navbar-query" >
        <h1>
            <slot name="Title"></slot>
        </h1>
        <div class="query-options" >
            <slot name="options" ></slot>
            <searchInput @inputChanged="onInputChanged" ></searchInput>
        </div>
    </div>
</template>

<script>
import searchInput from "@/components/interraction/inputs/search-input.vue"
export default{
    components : {
        searchInput
    },
    props : {
        theme : String
    },
    methods : {
        onInputChanged(inputToTransfer){
            this.$emit("input-changed",inputToTransfer);
        }
    }

}

</script>
<style >
.holder-navbar-query{
    width: 100%;
    height: 50px;

    border-radius: var(--small-border-radius);
    padding: var(--small-padding);
    box-sizing: border-box;

    display: flex;
    justify-content: space-between;
    align-items: center;
}
.query-options{
    display: flex;
    justify-content: space-between;
    align-items: center;

    gap:5px;
    font-weight: 500;
    font-size: 20px;
}
.query-options p{
    cursor: pointer;
}
.query-options p:hover{
    text-decoration: underline;
}

.flashy{
    background-color: var(--dark-color-1);
    color : var(--white-text-color);
}
.white{
    background-color: var(--light-color-0);
    color : var(--dark-text-color);
}


</style>