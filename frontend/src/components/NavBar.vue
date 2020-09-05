<template>
  <header>
    <div>
      <b-navbar toggleable="lg" type="light" variant="light">
        <b-container>
          <b-navbar-toggle target="nav-collapse" class="mr-auto"></b-navbar-toggle>
          <b-dropdown variant="link" right class="d-md-none">
            <template v-slot:button-content>
              <b-icon-plus></b-icon-plus>
            </template>
            <b-dropdown-item :to="{name: 'robot-create'}">机器人</b-dropdown-item>
            <b-dropdown-item :to="{name: 'strategy-create'}">策略</b-dropdown-item>
          </b-dropdown>
          <b-dropdown variant="link" right class="d-md-none">
            <template v-slot:button-content>
              <b-avatar size="sm"></b-avatar>
            </template>
            <b-dropdown-item to="/account">账户</b-dropdown-item>
            <b-dropdown-item to="/login" @click="logout">登出</b-dropdown-item>
          </b-dropdown>

          <b-collapse id="nav-collapse" is-nav>
            <b-navbar-brand href="#" class="d-none d-md-block">
              <b-icon-x-diamond scale="1.5"></b-icon-x-diamond>
            </b-navbar-brand>
            <b-navbar-nav class="mr-auto" v-if="isAuthenticated">
              <b-nav-item :to="{name: 'robot-list'}">机器人</b-nav-item>
              <b-nav-item :to="{name: 'strategy-list'}">策略</b-nav-item>
              <b-nav-item to="/connect">接入</b-nav-item>
            </b-navbar-nav>

            <template v-if="isAuthenticated">
              <b-dropdown variant="link" right class="d-none d-md-block">
                <template v-slot:button-content>
                  <b-icon-plus></b-icon-plus>
                </template>
                <b-dropdown-item :to="{name: 'robot-create'}">机器人</b-dropdown-item>
                <b-dropdown-item :to="{name: 'strategy-create'}">策略</b-dropdown-item>
              </b-dropdown>
              <b-dropdown variant="link" right class="d-none d-md-block" toggle-class="pr-0">
                <template v-slot:button-content>
                  <b-avatar size="sm"></b-avatar>
                </template>
                <b-dropdown-item to="/account">账户</b-dropdown-item>
                <b-dropdown-item to="/login" @click="logout">登出</b-dropdown-item>
              </b-dropdown>
            </template>
            <b-navbar-nav v-else class="ml-auto">
              <b-nav-item to="/login">登录</b-nav-item>
            </b-navbar-nav>

          </b-collapse>
        </b-container>
      </b-navbar>
    </div>
  </header>
</template>

<script>
import {mapGetters} from 'vuex'

export default {
  name: "NavBar",
  methods: {
    logout: function () {
      this.$store.commit("REMOVE_AUTH_TOKEN")
      this.$store.commit("REMOVE_USER")
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