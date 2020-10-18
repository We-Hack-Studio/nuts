<template>
    <!-- Sidebar -->
    <ul
        :class="[
            'navbar-nav',
            'bg-gradient-primary',
            'sidebar',
            'sidebar-dark',
            'accordion',
            isToggled ? 'toggled' : '',
        ]"
        id="accordionSidebar"
    >
        <!-- Sidebar - Brand -->
        <a class="sidebar-brand d-flex align-items-center justify-content-center" href="#">
            <div class="sidebar-brand-icon">
                <b-icon icon="x-diamond"></b-icon>
            </div>
            <div class="sidebar-brand-text mx-3">YUFU 量化</div>
        </a>

        <!-- Divider -->
        <hr class="sidebar-divider my-0" />

        <!-- Nav Item - Dashboard -->
        <b-nav-item class="nav-link" :to="{ name: 'robot-list' }">
            <b-icon icon="cpu" class="mr-2"></b-icon>
            <span>机器人</span>
        </b-nav-item>

        <!-- Divider -->
        <!-- <hr class="sidebar-divider"> -->

        <!-- Heading -->
        <!-- <div class="sidebar-heading">
        策略
      </div> -->

        <!-- Nav Item - Pages Collapse Menu -->
        <b-nav-item class="nav-link" :to="{ name: 'strategy-list' }">
            <b-icon icon="graph-up" class="mr-2"></b-icon>
            <span>策略</span>
        </b-nav-item>

        <!-- Divider -->
        <!-- <hr class="sidebar-divider"> -->

        <!-- Heading -->
        <!-- <div class="sidebar-heading">
        接入
      </div> -->

        <!-- Nav Item - Charts -->
        <b-nav-item class="nav-link" to="/connect">
            <b-icon icon="key" class="mr-2"></b-icon>
            <span>接入</span>
        </b-nav-item>
        <!-- <router-link to="/connect">接入</router-link> -->

        <!-- Divider -->
        <!-- <hr class="sidebar-divider d-none d-md-block"> -->

        <!-- Sidebar Toggler (Sidebar) -->
        <div class="text-center d-none d-md-inline">
            <!-- <button class="rounded-circle border-0" id="sidebarToggle" @click="sidebarToggle"></button> -->
            <b-button class="rounded-circle border-0 mt-3" id="sidebarToggle" @click="sidebarToggle">
                <b-icon :icon="isToggled ? 'chevron-right' : 'chevron-left'" class="toggle-icon"></b-icon>
            </b-button>
        </div>
    </ul>
    <!-- End of Sidebar -->
</template>

<script>
export default {
    props: ['isToggled'],
    methods: {
        sidebarToggle() {
            this.$emit('toggleSideBar');
        },
    },
};
</script>

<style lang="scss">
@import '../assets/sidebar.scss';

// .sidebar {
//     background: red;
// }
</style>
