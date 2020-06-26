<template>
  <div>
    <div>UID: {{userId}}</div>
    <div>用户名: {{username}}</div>
    <div class="" v-if="hideToken">
      <span class="mr-2">认证令牌: {{maskedToken}}</span>
      <b-icon-eye @click="hideToken=!hideToken"></b-icon-eye>
    </div>
    <div class="" v-if="!hideToken">
      <span class="mr-2">认证令牌: {{token}}</span>
      <b-icon-eye-slash @click="hideToken=!hideToken"></b-icon-eye-slash>
    </div>
  </div>
</template>

<script>
    import {mapState} from 'vuex'

    export default {
        data() {
            return {
                hideToken: true,
            }
        },
        computed: {
            ...mapState({
                userId: state => state.user.userId,
                username: state => state.user.username,
                nickname: state => state.user.nickname,
                token: state => state.user.token,
            }),
            maskedToken() {
                return '*'.repeat(this.token.length)
            },
        }
    }
</script>