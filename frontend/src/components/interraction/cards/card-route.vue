<template>
    <div class="card">
        <p class="header-card">
            <strong style="display: flex;justify-content: flex-start;align-items: center;gap:5px;" >
                <slot name="Titre" ></slot>
            </strong>
            <span class="card-icon" >
                <slot name="icon"></slot>
            </span>
        </p>
        <p class="description">
            <slot name="Description" ></slot>    
        </p>

    </div>
</template>
<script>
export default{
    name : 'cards-route'
}
</script>
<style scoped>
.router-link-temp{
    position: relative;

    height: 100%;
    width: 100%;

    background-color: red;
}
.card-icon{
    position: relative;

    cursor: pointer;
    transition: all 0.15s ease-out;
}
.card-icon:hover{
    scale: 1.2;
}
.card{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    
    background-color: var(--light-color-0);

    height: 100%;
    width: 100%;

    padding: var(--small-padding);
    box-sizing: border-box;

    border-bottom: solid 1px var(--gray-color-1);
    border-right: solid 1px var(--gray-color-1);
    
}
.card .header-card{
    width: 100%;

    display: flex;
    justify-content: space-between;
    align-items: center;

    color: black;
    font-size: 18px;
    font-weight: 500;
}
.description{
    overflow-y: auto;

    color:var(--dark-text-color );

    font-size: 14px;
}
.description::-webkit-scrollbar {
    width: 5px;
}

.description::-webkit-scrollbar-thumb {
    background-color: #999;
    border-radius: 5px;
}

.description::-webkit-scrollbar-track {
    background-color: #fff;
}
</style>