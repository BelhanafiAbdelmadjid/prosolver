/* -------------------------------------------------------------------------- */
/*                                  JSON DATA                                 */
/* -------------------------------------------------------------------------- */
/*  

servers : Array
[
{
    id : X , name : "test" , ip : "@ip" , status : "Active/Down"
}
]

*/

<template>
    <div class="table thin-scroll-bar">
        <table>
            <tr class="table-header" >
                <slot name="tableHeaders"></slot>
            </tr>
            <slot name="tableRows"></slot>
            
            <div style="width: 100%;height: 100%;"  >
                <slot name="tableLoadingAnimation"></slot>
            </div>

            <!-- <tr  v-for="server in servers" :key="server.id" >
                <td class="server-name">{{ server.name }}</td>
                <td>
                    <p>{{ server.ip }}</p>
                </td>
                <td>
                    <p class="holder-status">
                        <span :class="{ 'status-dot-active' : server.status == 'Active','status-dot-down' : server.status == 'Down'  }"  class="status-dot" ></span>
                        <span>{{ server.status }}</span>
                    </p>
                </td>
            </tr> -->

        </table>
    </div>
</template>
<script>
export default{
    name : "table-extension",
    data(){
        return{
            servers : []
        }
    },
    methods : {
        getServers(){
            this.servers = [
                {
                    id : 5,
                    name : "Onboarding01-uat",
                    ip : "192.168.1.104",
                    status : 'Active'
                },
                {
                    id : 15,
                    name : "Onboarding02-uat",
                    ip : "192.168.1.107",
                    status : 'Down'
                },
            ]
        }
    },
    beforeMount(){
        this.getServers();
    }
}
</script>
<style >
.table{
    max-height: 100%;
    overflow: auto;
}
.table table{
    
    width: 100%;
    

    background-color: var(--light-color-0);
    border-radius: var(--medieum-border-radius);

    border-collapse: collapse;

    overflow: hidden;

}
.table table  tr{
    height: 50px;

    border-bottom: solid 1px var(--gray-color-1 );
}
.table table tr td{
    padding-left: 15px;
    box-sizing: border-box;

    cursor: pointer;

}

.table table  tr td:nth-child(1){
    font-weight: 500;
}
.table .table-header{
    color: var(--white-text-color);
    background-color: var(--warm-color-0);
    font-weight: 500;
    cursor: default;
}
.holder-status{
    display: flex;
    justify-content: flex-start;
    align-items: center;

    gap: 3px;
}
.status-dot{

    height: 8px;
    width: 8px;

    border-radius: 50%;

    background-color: gray;
    opacity: 0.65;
}
.status-dot-down{
    background-color: var(--danger-color);
}
.status-dot-active{
    background-color: var(--validation-color);
}
</style>