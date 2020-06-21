<template>
  <b-card
          header="创建机器人"
          header-tag="header"
  >
    <b-form @submit="onSubmit">
      <b-form-group
              label="名字:"
              label-for="id_name"
      >
        <b-form-input
                id="id_name"
                v-model="form.name"
                type="text"
                required
        ></b-form-input>
      </b-form-group>
      <b-form-group label="交易所凭证:" label-for="id_credential">
        <b-form-select
                id="id_credential"
                v-model="form.credential"
                :options="credentialOptions"
                required
        ></b-form-select>
      </b-form-group>
      <b-form-group label="交易对:" label-for="id_pair">
        <b-form-input
                id="id_pair"
                v-model="form.pair"
                required
        ></b-form-input>
      </b-form-group>
      <b-form-group label="保证金币种:" label-for="id_margin_currency">
        <b-form-input
                id="id_margin_currency"
                v-model="form.marginCurrency"
                required
        ></b-form-input>
      </b-form-group>
      <b-form-checkbox
              id="id_enable"
              v-model="form.enable"
              name="enable"
              value=true
              unchecked-value=false
      >
        启用
      </b-form-checkbox>
      <b-button block type="submit" variant="primary" class="mt-3">创建</b-button>
    </b-form>
  </b-card>
</template>

<script>
    import {getCredentialList, createRobot} from "../api";

    export default {
        name: 'RobotForm',
        data() {
            return {
                form: {
                    name: '',
                    credential: null,
                    pair: '',
                    marginCurrency: '',
                    enable: false
                },
                credentialOptions: [],
            }
        },
        methods: {
            onSubmit(evt) {
                evt.preventDefault()
                let data = {
                    "name": this.form.name,
                    "credential": this.form.credential,
                    "pair": this.form.pair,
                    "margin_currency": this.form.marginCurrency,
                    "enable": this.form.enable,
                }
                createRobot(data).then(() => {
                    this.$emit("robot-created")
                    this.form = {
                        name: '',
                        credential: null,
                        pair: '',
                        marginCurrency: '',
                        enable: false
                    }
                }).catch(err => {
                    console.log(err.data);
                })
            },
            setCredentialOptions(data) {
                this.credentialOptions = data.map(cred => ({value: cred.id, text: cred.note}))
            }
        },
        mounted() {
            getCredentialList().then(response => {
                this.setCredentialOptions(response.data)
            }).catch(err => {
                this.$bvToast.toast(`无法获取交易所凭证数据，错误信息： ${err.data}`, {
                    title: '数据获取失败',
                    autoHideDelay: 3000,
                    toaster: 'b-toaster-top-center',
                    variant: 'danger',
                    appendToast: false
                });
            })
        },
    }
</script>