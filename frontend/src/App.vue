<template>
  <div id="app">
    <nav-bar></nav-bar>
    <side-bar></side-bar>

    <b-container class="mt-4">
      <router-view></router-view>
    </b-container>
  </div>
</template>

<script>
    import NavBar from "./components/NavBar";
    import SideBar from './components/SideBar';

    export default {
        name: 'App',
        components: {
            NavBar,
            SideBar
        }
    }
</script>

<style>

</style>
