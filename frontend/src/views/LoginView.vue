<template>
  <div>
    <b-row>
      <b-col sm="12" md="4" offset-md="4">
        <b-card title="登录">
          <b-form @submit="onSubmit">
            <b-alert :show="hasError" variant="danger">{{errorMsg}}</b-alert>
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
            <b-button type="submit" block variant="primary">登录</b-button>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
    import {login} from "../api";
    import userLocalStorage from "../utils";

    export default {
        data() {
            return {
                form: {
                    username: '',
                    password: '',
                },
                hasError: false,
                errorMsg: ''
            }
        },
        methods: {
            onSubmit(evt) {
                evt.preventDefault()
                login(this.form).then(response => {
                    let payload = {
                        userId: response.data.user.id,
                        username: response.data.user.username,
                        nickname: response.data.user.nickname,
                        token: response.data.key,
                    }
                    this.$store.commit("SET_USER", payload)
                    userLocalStorage.save(payload)
                    this.$router.push('/ranking')
                }).catch(err => {
                    let errData = err.response.data
                    this.hasError = true
                    this.errorMsg = errData['non_field_errors'][0]
                })
            },
        }
    }
</script>