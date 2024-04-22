<template>
  <navBar v-if="!hideNav" ></navBar>
  <router-view></router-view>
  <sideBarError></sideBarError>
</template>
<style src='./assets/css/main.css'></style>

<script>
import navBar from './components/navbars/nav-bar.vue';
import sideBarError from "@/components/errors/sidebar-error.vue"
export default {
  name: 'App',
  components: {
    navBar,
    sideBarError
  }
}
</script>

<style>
@media only screen and (max-width: 1000px) {
    
}

</style>
