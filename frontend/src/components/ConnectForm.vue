<template>
  <b-card header-tag="header">
    <template #header>
      <h6 class="mb-0">绑定交易所凭据</h6>
    </template>
    <b-card-text>
      <b-row class="">
        <b-col sm="12" md="9">
          <b-form @submit="onSubmit" class="form-row">
            <b-col md="4">
              <b-form-group label="交易所:" label-for="id_exchange">
                <b-form-select
                    id="id_exchange"
                    v-model="form.exchange"
                    :options="exchangeOptions"
                    required
                ></b-form-select>
              </b-form-group>
            </b-col>
            <b-col md="4">
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
            <b-col md="4">
              <b-form-group label="API Key:" label-for="id_api_key">
                <b-form-input
                    id="id_api_key"
                    v-model="form.apiKey"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>
            <b-col md="6">
              <b-form-group label="Secret:" label-for="id_secret">
                <b-form-input
                    id="id_secret"
                    v-model="form.secret"
                    type="password"
                    required
                ></b-form-input>
              </b-form-group>
            </b-col>
            <b-col md="6">
              <b-form-group label="Passphrase:" label-for="id_passphrase">
                <b-form-input
                    id="id_passphrase"
                    v-model="form.passphrase"
                    type="password"
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
            <b-col class="text-center">
              <b-button type="submit" variant="primary" class="mt-3">绑定此交易所凭据</b-button>
            </b-col>
          </b-form>
        </b-col>
        <b-col sm="12" md="3">
          这里放帮助文档
        </b-col>
      </b-row>
    </b-card-text>
  </b-card>
</template>

<script>
import {getExchanges, postCredentials} from "../api";
import formatterMixin from "@/mixins/formatter"

export default {
  name: "ConnectForm",
  data() {
    return {
      form: {
        note: '',
        apiKey: '',
        secret: '',
        passphrase: '',
        exchange: null,
        testNet: false,
      },
      exchangeOptions: [],
    }
  },
  mixins: [formatterMixin],
  methods: {
    async onSubmit(event) {
      event.preventDefault()
      let data = {
        "note": this.form.note,
        "api_key": this.form.apiKey,
        "secret": this.form.secret,
        "passphrase": this.form.passphrase,
        "exchange": this.form.exchange,
        "test_net": this.form.testNet,
      }
      try {
        await postCredentials(data)
        this.$bvToast.toast('交易所接入成功！', {
          title: '成功',
          autoHideDelay: 3000,
          toaster: 'b-toaster-top-center',
          variant: 'success',
          appendToast: false
        });
        this.$emit("credential-added")
        this.form = {
          note: '',
          apiKey: '',
          secret: '',
          exchange: null,
          testNet: false,
        }
      } catch (error) {
        if (error.response) {
          this.$bvToast.toast('接入失败', {
            title: '接入失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '接入失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        }
      }
    },
    setExchangeOptions(data) {
      this.exchangeOptions = data.map(e => ({value: e.id, text: e["name_zh"]}))
    },
    async getExchangeOptions() {
      try {
        const exchangesRes = await getExchanges()
        this.setExchangeOptions(exchangesRes.data)
      } catch (error) {
        if (error.response) {
          this.$bvToast.toast('无法获取可接入的交易所列表', {
            title: '无法获取可接入的交易所列表',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '无法获取可接入的交易所列表',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        }
      }
    }
  },
  async mounted() {
    await this.getExchangeOptions()
  },
}
</script>