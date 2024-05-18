<template>
    <div class="global-input input-holder">
        <slot name="inputs" ></slot>
    </div>
</template>
<script>
export default {

}
</script>
<style >
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

</style>