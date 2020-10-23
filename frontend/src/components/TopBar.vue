<template>
    <!-- Topbar -->
    <nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">
        <!-- Sidebar Toggle (Topbar) -->
        <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3" @click="toggleSideBar">
            <b-icon icon="justify"></b-icon>
        </button>

        <!-- Topbar Navbar -->
        <ul class="navbar-nav ml-auto">
            <div class="topbar-divider"></div>

            <!-- Nav Item - User Information -->
            <li class="nav-item dropdown no-arrow">
                <b-dropdown variant="link" right class="nav-link" toggle-class="pr-0">
                    <template v-slot:button-content>
                        <b-avatar size="large" class="mt-2"></b-avatar>
                    </template>
                    <b-dropdown-item to="/account">
                        <b-icon icon="person-bounding-box" class="mr-1" /> 账户
                    </b-dropdown-item>
                    <b-dropdown-divider></b-dropdown-divider>
                    <b-dropdown-item to="/login"> <b-icon icon="box-arrow-right" class="mr-1" /> 登出 </b-dropdown-item>
                </b-dropdown>
            </li>
        </ul>
    </nav>
    <!-- End of Topbar -->
</template>

<script>
export default {
    props: ['isToggled'],
    methods: {
        toggleSideBar() {
            this.$emit('toggleSideBar');
        },
    },
};
</script>

<style></style>
