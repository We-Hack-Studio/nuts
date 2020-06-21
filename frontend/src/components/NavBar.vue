<template>
  <header>
    <div>
      <b-navbar toggleable="lg" type="dark" variant="info">
        <b-navbar-brand href="#">NavBar</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item to="/ranking">排行</b-nav-item>
            <b-nav-item to="/robot/list" v-if="isAuthenticated">机器人</b-nav-item>
            <b-nav-item to="/connect" v-if="isAuthenticated">接入</b-nav-item>
          </b-navbar-nav>
          <b-navbar-nav class="ml-auto">
            <b-nav-item to="/login" v-if="isAuthenticated" @click="logout">登出</b-nav-item>
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