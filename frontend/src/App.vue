<template>
    <div id="app">
        <side-bar @toggleSideBar="handleToggleSideBar" :isToggled="isToggled"></side-bar>
        <div class="content-wrapper">
            <top-bar class="mb-4" @toggleSideBar="handleToggleSideBar" :isToggled="isToggled"></top-bar>
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
import TopBar from './components/TopBar';
import SideBar from './components/SideBar';

export default {
    name: 'App',
    data() {
        return {
            isToggled: false,
        };
    },
    mounted() {
        window.onresize = () => {
            const width = document.documentElement.clientWidth;
            this.isToggled = width > 576 ? false : true;
        };
    },
    components: {
        TopBar,
        SideBar,
    },
    methods: {
        handleToggleSideBar() {
            this.isToggled = !this.isToggled;
        },
    },
};
</script>

<style lang="scss">
@import './assets/nav.scss';
#app {
    display: flex;
}
.content-wrapper {
    width: 100%;
}
</style>
