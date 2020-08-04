<template>
  <header>
    <div>
      <b-navbar toggleable="lg" type="light" variant="light">
        <b-navbar-brand href="#">
          <b-icon-x-diamond scale="1.5"></b-icon-x-diamond>
        </b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item to="/robot/list" v-if="isAuthenticated">机器人</b-nav-item>
            <b-nav-item to="/strategy-template/list" v-if="isAuthenticated">策略</b-nav-item>
            <b-nav-item to="/connect" v-if="isAuthenticated">接入</b-nav-item>
          </b-navbar-nav>
          <b-navbar-nav class="ml-auto">
            <b-nav-item-dropdown right v-if="isAuthenticated" class="mr-2">
              <!-- Using 'button-content' slot -->
              <template v-slot:button-content>
                <b-icon-plus></b-icon-plus>
              </template>
              <b-dropdown-item to="/robot/create">机器人</b-dropdown-item>
              <b-dropdown-item to="/strategy-template/create">策略模板</b-dropdown-item>
            </b-nav-item-dropdown>
            <b-nav-item-dropdown right v-if="isAuthenticated">
              <!-- Using 'button-content' slot -->
              <template v-slot:button-content>
                <b-avatar size="sm"></b-avatar>
              </template>
              <b-dropdown-item to="/account">账户</b-dropdown-item>
              <b-dropdown-item to="/login" @click="logout">登出</b-dropdown-item>
            </b-nav-item-dropdown>
            <b-nav-item to="/login" v-else>登录</b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
  </header>
</template>

<script>
    import {mapGetters} from 'vuex'
    import userLocalStorage from "../utils";

    export default {
        name: "NavBar",
        methods: {
            logout: function () {
                this.$store.commit("REMOVE_USER")
                userLocalStorage.clear()
            }
        },
        computed: {
            ...mapGetters([
                'isAuthenticated',
            ])
        }
    }
</script>

<style scoped>

</style>