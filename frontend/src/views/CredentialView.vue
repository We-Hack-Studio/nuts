<template>
  <div class="mx-3">
    <b-card header-tag="header">
      <template #header>
        <h6 class="mb-0">绑定交易所凭据</h6>
      </template>
      <b-card-text>
        <b-row class="">
          <b-col sm="12" md="9">
            <credential-form :exchange-options="exchangeOptions" :form-initial="credentialFormInitial"
                             @submitted="getCredentialList"></credential-form>
          </b-col>
          <b-col sm="12" md="3">
            <credential-helper></credential-helper>
          </b-col>
        </b-row>
      </b-card-text>
    </b-card>
    <b-row class="mt-4">
      <b-col sm="12" md="6" lg="4" class="mb-3" v-for="credential in credentialList" :key="credential.credId">
        <credential-item :credential="credential" @delete-confirmed="deleteCredential"
                         @edit="setCredentialFormInitial"></credential-item>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import CredentialForm from "@/components/CredentialForm"
import CredentialHelper from "@/components/CredentialHelper"
import CredentialItem from "@/components/CredentialItem"
import {getCredentials, deleteCredential} from "@/api/credential"
import {getExchanges} from "@/api"

export default {
  name: "CredentialView",
  data() {
    return {
      credentialList: [],
      exchangeOptions: [],
      credentialFormInitial: null,
    }
  },
  components: {
    CredentialForm,
    CredentialItem,
    CredentialHelper,
  },
  methods: {
    async getExchangeList() {
      try {
        const exchangesRes = await getExchanges()
        this.exchangeOptions = exchangesRes.data.map(e => ({value: e.id, text: e['name_zh']}))
      } catch (error) {
        if (error.response) {
          this.$bvToast.toast('获取可接入交易所列表失败', {
            title: '获取可接入交易所列表失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '获取可接入交易所列表失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false
          });
        }
      }
    },
    async getCredentialList() {
      try {
        const credentialsRes = await getCredentials()
        this.credentialList = credentialsRes.data.map(cred => ({
          credId: cred.id,
          exchangeNameZh: cred.exchange['name_zh'],
          exchangeId: cred.exchange.id,
          note: cred.note,
          apiKey: cred['api_key'],
          secret: cred.secret,
          passphrase: cred.passphrase,
          testNet: cred['test_net'],
          createdAt: cred['created_at'],
        }))
      } catch (error) {
        if (error.response) {
          this.$bvToast.toast('获取已绑定交易所凭据列表失败', {
            title: '获取已绑定交易所凭据列表失败',
            autoHideDelay: 2000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '获取已绑定交易所凭据列表失败',
            autoHideDelay: 2000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false
          });
        }
      }
    },
    async deleteCredential({credId}) {
      try {
        await deleteCredential(credId)
        await this.getCredentialList()
      } catch (error) {
        if (error.response) {
          this.$bvToast.toast('交易所凭据删除失败', {
            title: '交易所凭据删除失败',
            autoHideDelay: 2000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '交易所凭据删除失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false
          });
        }
      }
    },
    async handleCredentialFormSubmit() {
      await this.getCredentialList()
    },
    setCredentialFormInitial({initial}) {
      this.credentialFormInitial = initial
    }
  },
  async mounted() {
    await this.getCredentialList()
    await this.getExchangeList()
  },
}
</script>

