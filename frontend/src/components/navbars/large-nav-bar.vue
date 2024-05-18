<template>
    <nav>
        <div v-if="connexionType"  :class="{'connected-color-prod' : connexionType=='Prod','connected-color-uat' : connexionType=='UAT'}"  class="connected">
            <p  class="connected-type" >
                {{ connexionType }}
            </p>
            <div @click="disconnect" class="connected-dot" >
                <svg  width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M13 4.00897C13 3.74376 12.8947 3.4894 12.7071 3.30187C12.5196 3.11433 12.2652 3.00897 12 3.00897C11.7348 3.00897 11.4804 3.11433 11.2929 3.30187C11.1054 3.4894 11 3.74376 11 4.00897L10.997 12.012C10.997 12.2772 11.1024 12.5315 11.2899 12.7191C11.4774 12.9066 11.7318 13.012 11.997 13.012C12.2622 13.012 12.5166 12.9066 12.7041 12.7191C12.8917 12.5315 12.997 12.2772 12.997 12.012L13 4.00897Z" fill="white"/>
                    <path d="M4 12.992C4 10.782 4.895 8.78196 6.343 7.33496L7.757 8.74896C6.91785 9.58806 6.34636 10.6572 6.11482 11.8211C5.88327 12.985 6.00207 14.1914 6.45618 15.2878C6.9103 16.3841 7.67933 17.3212 8.66604 17.9805C9.65274 18.6398 10.8128 18.9917 11.9995 18.9917C13.1862 18.9917 14.3463 18.6398 15.333 17.9805C16.3197 17.3212 17.0887 16.3841 17.5428 15.2878C17.9969 14.1914 18.1157 12.985 17.8842 11.8211C17.6526 10.6572 17.0812 9.58806 16.242 8.74896L17.657 7.33496C18.5872 8.26525 19.2737 9.41058 19.6556 10.6695C20.0374 11.9285 20.1029 13.2622 19.8463 14.5525C19.5896 15.8428 19.0187 17.0499 18.1841 18.0668C17.3495 19.0838 16.2769 19.8792 15.0615 20.3827C13.8461 20.8861 12.5252 21.0821 11.216 20.9532C9.90671 20.8242 8.64946 20.3744 7.55558 19.6435C6.46169 18.9126 5.56493 17.9233 4.94474 16.763C4.32454 15.6028 4.00005 14.3075 4 12.992Z" fill="white"/>
                </svg>
            </div>
        </div>
        <div class="list" >
            <listing>
                <template v-slot:header>Supervision</template>
                <template v-slot:list>
                    <li>
                        <RouterLink    :to="{ name: 'supervision', query: { UAT : true  }}"  >UAT</RouterLink>
                    </li>
                    <li>
                        <RouterLink  @click="console.log('clicked')" :to="{ name: 'supervision', query: { Prod : true  }}"  >PROD</RouterLink>
                    </li>
                </template>
            </listing>
            <listing v-if="userType == 'Admin' || userType == 'Worker' " >
                <template v-slot:header>Incidents</template>
                <template v-slot:list>
                    <li><RouterLink    :to="{ name: 'incidentsList'}"  >List</RouterLink></li>

                    <listing  >
                        <template v-slot:header>Settings</template>
                        <template v-slot:list>
                            <li>
                                <RouterLink    :to="{ name: 'serverList'}"  >Servers</RouterLink>
                            </li>
                            <li>
                                <RouterLink   :to="{ name: 'scriptList'}"  >Scripts</RouterLink>
                            </li>
                            <li v-if="userType == 'Admin'"  >
                                <RouterLink    :to="{ name: 'users'}"  >Users</RouterLink>
                            </li>
                        </template>
                    </listing>

                </template>
            </listing>
        </div>
    </nav>
</template>
<script>
import listing from "@/components/navbars/UI/listing-elements.vue"
export default{
    components : {
        listing
    },
    data(){
        return {
        }
    },
    props : {
        'connexionType' : String,
        'userType' : String
    },
    methods : {
        disconnect(){
            this.$emit("logout");
        }
    }
}
</script>
<style scoped>
nav{
    width: var(--navbar-width);
    height: 100vh;

    background-color: var(--light-color-1);

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
}
.list{
    width: 100%;

    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap:10px;

    padding: 5px;
    box-sizing: border-box;
}
.connected{
    position: relative;
    
    width:100%;
    
    padding : 4px;
    box-sizing: border-box;

    display: flex;
    justify-content: space-between;
    align-items: center;
    

}
.connected-color-uat{
    background-color: var(--dark-color);
}
.connected-color-prod{
    background-color: var(--PROD-primary-color );
}
.connected-type{
    font-weight: 500;
    font-size:20px;
    color: rgb(255, 255, 255)
}
.connected-dot{
    width: 17px;
    height: 17px;
    border-radius: 50%;
    background-color: var(--UAT-attention-color);
    display:  flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}
</style>