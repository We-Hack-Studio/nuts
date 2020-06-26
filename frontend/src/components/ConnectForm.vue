<template>
  <b-form @submit="onSubmit" class="form-row">
    <b-col md="3">
      <b-form-group label="交易所:" label-for="id_exchange">
        <b-form-select
                id="id_exchange"
                v-model="form.exchange"
                :options="exchangeOptions"
                required
        ></b-form-select>
      </b-form-group>
    </b-col>
    <b-col md="3">
      <b-form-group
              label="备注:"
              label-for="id_note"
      >
        <b-form-input
                id="id_note"
                v-model="form.note"
                type="text"
                required
        ></b-form-input>
      </b-form-group>
    </b-col>
    <b-col md="6">
      <b-form-group label="API Key:" label-for="id_api_key">
        <b-form-input
                id="id_api_key"
                v-model="form.apiKey"
                required
        ></b-form-input>
      </b-form-group>
    </b-col>
    <b-col md="12">
      <b-form-group label="Secret:" label-for="id_secret">
        <b-form-input
                id="id_secret"
                v-model="form.secret"
                type="password"
                required
        ></b-form-input>
      </b-form-group>
    </b-col>
    <b-col md="12">
      <b-form-checkbox
              id="id_test_net"
              v-model="form.testNet"
              name="test_net"
              value="true"
              unchecked-value="false"
      >
        测试网
      </b-form-checkbox>
    </b-col>
    <b-col>
      <b-button type="submit" variant="primary" class="mt-2">接入</b-button>
    </b-col>
  </b-form>
</template>

<script>
    import {getExchangeList, createCredential} from "../api";

    export default {
        name: "ConnectForm",
        data() {
            return {
                form: {
                    note: '',
                    apiKey: '',
                    secret: '',
                    exchange: null,
                    testNet: false,
                },
                exchangeOptions: [],
            }
        },
        methods: {
            onSubmit(evt) {
                evt.preventDefault()
                let data = {
                    "note": this.form.note,
                    "api_key": this.form.apiKey,
                    "secret": this.form.secret,
                    "exchange": this.form.exchange,
                    "test_net": this.form.testNet,
                }
                createCredential(data).then(response => {
                    let cred = response.data
                    let payload = {
                        credId: cred.id,
                        exchangeNameZh: cred['exchange_info']['name_zh'],
                        note: cred.note,
                        apiKeyMasked: cred['api_key_masked'],
                        secretMasked: cred['secret_masked'],
                        createdAt: cred['created_at'],
                    }
                    this.$emit("credential-added", payload)
                    this.form = {
                        note: '',
                        apiKey: '',
                        secret: '',
                        exchange: null,
                        testNet: false,
                    }
                }).catch(err => {
                    console.log(err.data);
                })
            },
            setExchangeOptions(data) {
                this.exchangeOptions = data.map(e => ({value: e.id, text: e["name_zh"]}))
            }
        },
        mounted() {
            getExchangeList().then(response => {
                this.setExchangeOptions(response.data)
            }).catch(err => {
                this.$bvToast.toast(`无法获取可接入的交易所数据，错误信息： ${err.data}`, {
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