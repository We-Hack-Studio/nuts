<template>
  <div id="app">
    <side-bar></side-bar>
    <div class="content-wrapper">
      <nav-bar class="mb-4"></nav-bar>
      <router-view></router-view>
    </div>
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
#app {
  display: flex;
}
.content-wrapper {
  width: 100%;
}
</style>
