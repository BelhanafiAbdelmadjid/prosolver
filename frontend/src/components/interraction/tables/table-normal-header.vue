<template>
    <div class="table thin-scroll-bar">
        <table>
            <tr class="header">
                <slot name="tableHeaders"></slot>
            </tr>

            <slot name="tableRows"></slot>


        </table>
    </div>
</template>
<script>
export default{
    name : 'table-simple-header',
    data(){
        return{

        }
    }
}
</script>
<style>
.table table{
    width: 100%;
    background-color: white;
    border-radius: 5px;

    border-collapse: collapse;
}
.table table thead tr{
    height: 50px;
}
tr {
  border-bottom: 1px solid #ddd;
  height: 60px;
  width: 100%;
}
tr:hover {
    background-color: rgb(228, 228, 228);
}
tr td{
    padding: 5px;
    box-sizing: border-box;
}
.header:hover{
    background-color: none;
}
</style>