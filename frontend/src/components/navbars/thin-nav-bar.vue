<template>
    <nav>
        <div class="callout-nav" @click="openNav=true" >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <g clip-path="url(#clip0_87_2)">
                    <path
                        d="M20 17.5C20.3852 17.5002 20.7556 17.6486 21.0344 17.9144C21.3132 18.1802 21.479 18.5431 21.4975 18.9279C21.516 19.3127 21.3858 19.6898 21.1338 19.9812C20.8818 20.2726 20.5274 20.4558 20.144 20.493L20 20.5H4C3.61478 20.4998 3.24441 20.3514 2.96561 20.0856C2.68682 19.8198 2.52099 19.4569 2.50248 19.0721C2.48396 18.6873 2.61419 18.3102 2.86618 18.0188C3.11816 17.7274 3.47258 17.5442 3.856 17.507L4 17.5H20ZM20 10.5C20.3978 10.5 20.7794 10.658 21.0607 10.9393C21.342 11.2206 21.5 11.6022 21.5 12C21.5 12.3978 21.342 12.7794 21.0607 13.0607C20.7794 13.342 20.3978 13.5 20 13.5H4C3.60218 13.5 3.22064 13.342 2.93934 13.0607C2.65804 12.7794 2.5 12.3978 2.5 12C2.5 11.6022 2.65804 11.2206 2.93934 10.9393C3.22064 10.658 3.60218 10.5 4 10.5H20ZM20 3.5C20.3978 3.5 20.7794 3.65804 21.0607 3.93934C21.342 4.22064 21.5 4.60218 21.5 5C21.5 5.39782 21.342 5.77936 21.0607 6.06066C20.7794 6.34196 20.3978 6.5 20 6.5H4C3.60218 6.5 3.22064 6.34196 2.93934 6.06066C2.65804 5.77936 2.5 5.39782 2.5 5C2.5 4.60218 2.65804 4.22064 2.93934 3.93934C3.22064 3.65804 3.60218 3.5 4 3.5H20Z"
                        fill="#222222" />
                </g>
                <defs>
                    <clipPath id="clip0_87_2">
                        <rect width="24" height="24" fill="white" />
                    </clipPath>
                </defs>
            </svg>
            <div  v-if="connexionType"  :class="{'connected-color-prod' : connexionType=='Prod','connected-color-uat' : connexionType=='UAT'}"  class="connected-callout">
                <p  class="connected-type" >
                    {{ connexionType }}
                </p>
                <div @click="disconnect" class="connected-dot-callout" >
                    <svg  width="16" height="16" viewBox="0 0 24 24" fill="none">
                        <path d="M13 4.00897C13 3.74376 12.8947 3.4894 12.7071 3.30187C12.5196 3.11433 12.2652 3.00897 12 3.00897C11.7348 3.00897 11.4804 3.11433 11.2929 3.30187C11.1054 3.4894 11 3.74376 11 4.00897L10.997 12.012C10.997 12.2772 11.1024 12.5315 11.2899 12.7191C11.4774 12.9066 11.7318 13.012 11.997 13.012C12.2622 13.012 12.5166 12.9066 12.7041 12.7191C12.8917 12.5315 12.997 12.2772 12.997 12.012L13 4.00897Z" fill="white"/>
                        <path d="M4 12.992C4 10.782 4.895 8.78196 6.343 7.33496L7.757 8.74896C6.91785 9.58806 6.34636 10.6572 6.11482 11.8211C5.88327 12.985 6.00207 14.1914 6.45618 15.2878C6.9103 16.3841 7.67933 17.3212 8.66604 17.9805C9.65274 18.6398 10.8128 18.9917 11.9995 18.9917C13.1862 18.9917 14.3463 18.6398 15.333 17.9805C16.3197 17.3212 17.0887 16.3841 17.5428 15.2878C17.9969 14.1914 18.1157 12.985 17.8842 11.8211C17.6526 10.6572 17.0812 9.58806 16.242 8.74896L17.657 7.33496C18.5872 8.26525 19.2737 9.41058 19.6556 10.6695C20.0374 11.9285 20.1029 13.2622 19.8463 14.5525C19.5896 15.8428 19.0187 17.0499 18.1841 18.0668C17.3495 19.0838 16.2769 19.8792 15.0615 20.3827C13.8461 20.8861 12.5252 21.0821 11.216 20.9532C9.90671 20.8242 8.64946 20.3744 7.55558 19.6435C6.46169 18.9126 5.56493 17.9233 4.94474 16.763C4.32454 15.6028 4.00005 14.3075 4 12.992Z" fill="white"/>
                    </svg>
                </div>
            </div>
        </div>
        <div  :class="{ 'open-nav': openNav, 'close-nav': !openNav }" class="large-nav" >
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
                            <RouterLink   :to="{ name: 'supervision', query: { Prod : true  }}"  >PROD</RouterLink>
                        </li>
                    </template>
                </listing>
                <listing  v-if="userType == 'Admin' || userType == 'Worker' " >
                    <template v-slot:header>Incidents</template>
                    <template v-slot:list>
                        <li><RouterLink    :to="{ name: 'incidentsList'}"  >List</RouterLink></li>

                        <listing>
                            <template v-if="userType == 'Admin'" v-slot:header>Settings</template>
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
        </div>
        <div v-show="openNav" @click="openNav=false" :class="{'overlay-active' : openNav}" class="overlay">
            <svg :class="{'close-icon-open':openNav}" class="close-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M18.3 5.71001C18.2075 5.61731 18.0976 5.54376 17.9766 5.49358C17.8557 5.4434 17.726 5.41757 17.595 5.41757C17.464 5.41757 17.3344 5.4434 17.2134 5.49358C17.0924 5.54376 16.9825 5.61731 16.89 5.71001L12 10.59L7.11001 5.70001C7.01743 5.60743 6.90752 5.53399 6.78655 5.48388C6.66559 5.43378 6.53594 5.40799 6.40501 5.40799C6.27408 5.40799 6.14443 5.43378 6.02347 5.48388C5.9025 5.53399 5.79259 5.60743 5.70001 5.70001C5.60743 5.79259 5.53399 5.9025 5.48388 6.02347C5.43378 6.14443 5.40799 6.27408 5.40799 6.40501C5.40799 6.53594 5.43378 6.66559 5.48388 6.78655C5.53399 6.90752 5.60743 7.01743 5.70001 7.11001L10.59 12L5.70001 16.89C5.60743 16.9826 5.53399 17.0925 5.48388 17.2135C5.43378 17.3344 5.40799 17.4641 5.40799 17.595C5.40799 17.7259 5.43378 17.8556 5.48388 17.9766C5.53399 18.0975 5.60743 18.2074 5.70001 18.3C5.79259 18.3926 5.9025 18.466 6.02347 18.5161C6.14443 18.5662 6.27408 18.592 6.40501 18.592C6.53594 18.592 6.66559 18.5662 6.78655 18.5161C6.90752 18.466 7.01743 18.3926 7.11001 18.3L12 13.41L16.89 18.3C16.9826 18.3926 17.0925 18.466 17.2135 18.5161C17.3344 18.5662 17.4641 18.592 17.595 18.592C17.7259 18.592 17.8556 18.5662 17.9766 18.5161C18.0975 18.466 18.2074 18.3926 18.3 18.3C18.3926 18.2074 18.466 18.0975 18.5161 17.9766C18.5662 17.8556 18.592 17.7259 18.592 17.595C18.592 17.4641 18.5662 17.3344 18.5161 17.2135C18.466 17.0925 18.3926 16.9826 18.3 16.89L13.41 12L18.3 7.11001C18.68 6.73001 18.68 6.09001 18.3 5.71001Z"
                    fill="#222222" />
            </svg>
        </div>
    </nav>
</template>
<script>
import listing from './UI/listing-elements.vue';
export default{
    data () {
        return{
            openNav: false,
        }
    },
    components : {
        listing
    },
    props : {
        "connexionType" : String
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
    position: fixed;
    top: 0;
    left: 0;

    height: var(--navbar-thin-height);
    width: 100%;

    background-color: var(--light-color-1);

    display: flex;
    justify-content: space-between;
    align-items: center;

    padding: 10px;
    box-sizing: border-box;

    box-shadow: 2px 0px 4px rgba(0, 0, 0, 0.1);

}
.large-nav{
    position: fixed;

    left: -100%;
    top: 0;
    z-index: 1000;

    height: 100vh;
    width: var(--navbar-width);

    transition: left 0.5s ease;


    background-color: var(--light-color-1);

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;

    box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.3);
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
.close-nav{
    left: -100%;
}
.open-nav{
    left: 0%;
}
nav .overlay{
    position: fixed;
    left: 0;
    top: 0;
    width: 100vw;
    height: 100vh;

    z-index: -9999;
    background-color: transparent;
    transition: background-color 1s;
}
nav .overlay-active{
    z-index: 999;
    background-color: rgba(49, 49, 49, 0.366);

}
.close-icon{
    position: fixed;
    left: -100%;

    opacity: 0;
    transition: all 0.5s ease;
}
.close-icon-open{
    left: var(--navbar-width);
    opacity: 1;
}
.callout-nav{
    display: flex;
    justify-content: space-between;
    align-items: center;

    width: 100%;
}
.connected-callout{
    position: relative;
    
    font-size: 12px;
    
    padding : 4px;
    box-sizing: border-box;

    display: flex;
    justify-content: space-between;
    align-items: center;
    
    width: 15%;
    height: 25px;
    border-radius: 5px;


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
    width: 23px;
    height: 23px;
    border-radius: 50%;
    background-color: var(--UAT-attention-color);
    display:  flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}
.connected-dot-callout{
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