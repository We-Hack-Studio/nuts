<template>
  <b-form @submit="onSubmit" class="form-row">
    <!--  Exchanges  -->
    <b-col md="4">
      <b-form-group label="交易所:" label-for="id_exchange">
        <b-form-select
            id="id_exchange"
            v-model="form.exchange"
            :options="exchangeOptions"
            required
            :disabled="disableExchange"
            :state="formErrors.exchange===undefined?null:false"
        ></b-form-select>
        <b-form-invalid-feedback :state="formErrors.exchange===undefined?null:false">
          {{ formErrors.exchange !== undefined && formErrors.exchange[0] }}
        </b-form-invalid-feedback>
      </b-form-group>
    </b-col>

    <!--  Note  -->
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
            :state="formErrors.note===undefined?null:false"
        ></b-form-input>
        <b-form-invalid-feedback :state="formErrors.note===undefined?null:false">
          {{ formErrors.note !== undefined && formErrors.note[0] }}
        </b-form-invalid-feedback>
      </b-form-group>
    </b-col>

    <!--  API Key  -->
    <b-col md="4">
      <b-form-group label="API Key:" label-for="id_api_key">
        <b-form-input
            id="id_api_key"
            v-model="form.apiKey"
            required
            autocomplete="new-password"
            :state="formErrors['api_key']===undefined?null:false"
        ></b-form-input>
        <b-form-invalid-feedback :state="formErrors['api_key']===undefined?null:false">
          {{ formErrors['api_key'] !== undefined && formErrors['api_key'][0] }}
        </b-form-invalid-feedback>
      </b-form-group>
    </b-col>

    <!--  Secret  -->
    <b-col md="6">
      <b-form-group label="Secret:" label-for="id_secret">
        <b-form-input
            id="id_secret"
            v-model="form.secret"
            type="password"
            required
            autocomplete="new-password"
        ></b-form-input>
      </b-form-group>
    </b-col>

    <!--  Passphrase  -->
    <b-col md="6">
      <b-form-group label="Passphrase:" label-for="id_passphrase">
        <b-form-input
            id="id_passphrase"
            v-model="form.passphrase"
            type="password"
            autocomplete="new-password"
        ></b-form-input>
      </b-form-group>
    </b-col>

    <!--  Test net  -->
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
    <b-col class="text-center mt-3">
      <b-button type="submit" variant="primary" class="mr-3">{{ editing ? "更新" : "绑定" }}</b-button>
      <b-button type="button" variant="danger" @click="reset">清空</b-button>
    </b-col>
  </b-form>
</template>

<script>

import {createCredential, updateCredential} from "@/api/credential";

export default {
  name: "CredentialForm",
  props: {
    formInitial: {
      type: Object,
      default: null
    },
    exchangeOptions: {
      type: Array,
      default: () => []
    },
  },
  data() {
    return {
      form: {
        credentialId: null,
        note: '',
        apiKey: '',
        secret: '',
        passphrase: '',
        exchange: null,
        testNet: false,
      },
      formErrors: {},
      disableExchange: false,
      editing: false,
    }
  },
  watch: {
    formInitial: function (val) {
      if (val !== null) {
        this.reset()
        this.form = Object.assign({}, this.form, this.formInitial)
        this.disableExchange = true
        this.editing = true
      }
    }
  },
  methods: {
    reset() {
      this.form = {
        credentialId: null,
        note: '',
        apiKey: '',
        secret: '',
        passphrase: '',
        exchange: null,
        testNet: false,
      }
      this.editing = false
      this.disableExchange = false
      this.formErrors = {}
    },
    async onSubmit(event) {
      event.preventDefault()
      if (this.form.credentialId === null) {
        await this.create()
      } else {
        await this.update()
      }
    },
    async create() {
      let data = {
        "note": this.form.note,
        "api_key": this.form.apiKey,
        "secret": this.form.secret,
        "passphrase": this.form.passphrase,
        "exchange": this.form.exchange,
        "test_net": this.form.testNet,
      }
      try {
        await createCredential(data)
        this.$bvToast.toast('交易所凭据绑定成功', {
          title: '交易所凭据绑定成功',
          autoHideDelay: 2000,
          toaster: 'b-toaster-top-right',
          variant: 'success',
          appendToast: false
        });
        this.reset()
        this.$emit("submitted")
      } catch (error) {
        if (error.response) {
          if (error.response.status === 400) {
            // form validation error
            this.formErrors = error.response.data
            return
          }
          // other errors
          this.$bvToast.toast('交易所凭据绑定失败', {
            title: '交易所凭据绑定失败',
            autoHideDelay: 2000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '交易所凭据绑定失败',
            autoHideDelay: 2000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false
          });
        }
      }
    },
    async update() {
      let data = {
        "note": this.form.note,
        "api_key": this.form.apiKey,
        "secret": this.form.secret,
        "passphrase": this.form.passphrase,
        "exchange": this.form.exchange,
        "test_net": this.form.testNet,
      }
      try {
        await updateCredential(this.form.credentialId, data)
        this.$bvToast.toast('交易所凭据更新成功', {
          title: '交易所凭据更新成功',
          autoHideDelay: 2000,
          toaster: 'b-toaster-top-right',
          variant: 'success',
          appendToast: false
        });
        this.editing = false
        this.disableExchange = false
        this.reset()
        this.$emit("submitted")
      } catch (error) {
        if (error.response) {
          if (error.response.status === 400) {
            // form validation error
            this.formErrors = error.response.data
            return
          }
          this.$bvToast.toast('交易所凭据更新失败', {
            title: '交易所凭据更新失败',
            autoHideDelay: 2000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '交易所凭据更新失败',
            autoHideDelay: 2000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false
          });
        }
      }
    },
  },
}
</script>