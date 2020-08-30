<template>
  <div>
    <b-row>
      <b-col sm="12" md="4" offset-md="4">
        <b-card title="登录">
          <b-form @submit="onSubmit">
            <b-alert :show="hasError" variant="danger">{{ errorMsg }}</b-alert>
            <b-form-group
                label="用户名:"
                label-for="id_username"
            >
              <b-form-input
                  id="id_username"
                  v-model="form.username"
                  type="text"
                  required
              ></b-form-input>
            </b-form-group>
            <b-form-group label="密码:" label-for="id_password">
              <b-form-input
                  id="id_password"
                  v-model="form.password"
                  type="password"
                  required
              ></b-form-input>
            </b-form-group>
            <b-button type="submit" block variant="primary" :disabled="formProcessing">登录</b-button>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import {getUsersMe, postAuthLogin} from "../api";

export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      hasError: false,
      errorMsg: '',
      formProcessing: false,
    }
  },
  methods: {
    async onSubmit(evt) {
      this.formProcessing = true
      evt.preventDefault()
      try {
        const loginRes = await postAuthLogin(this.form)
        const authToken = loginRes.data["auth_token"]
        this.$store.commit("SET_AUTH_TOKEN", authToken)

        const usersMeRes = await getUsersMe()
        console.log(usersMeRes)
        const user = {
          userId: usersMeRes.data.id,
          username: usersMeRes.data.username,
          nickname: usersMeRes.data.nickname
        }
        this.$store.commit("SET_USER", user)
        this.formProcessing = false
        await this.$router.push({name: 'robot-list'})
      } catch (error) {
        if (error.response) {
          if (error.response.status === 500) {
            this.$bvToast.toast('服务端错误', {
              title: '登录失败',
              autoHideDelay: 3000,
              toaster: 'b-toaster-top-center',
              variant: 'danger',
              appendToast: false
            });
          } else if (error.response.status === 400) {
            // form validation error
            let errData = error.response.data
            this.hasError = true
            this.errorMsg = errData['non_field_errors'][0]
          }
        } else {
          this.$bvToast.toast(error.message, {
            title: '登录失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        }
        this.$store.commit("REMOVE_AUTH_TOKEN")
        this.$store.commit("REMOVE_USER")
        this.formProcessing = false
      }
    }
  }
}
</script>

