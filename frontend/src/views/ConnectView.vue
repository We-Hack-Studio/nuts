<template>
  <div class="mx-3">
    <connect-form @credential-added="getCredentialList"></connect-form>
    <connected-table :credential-list="credentialList" @delete-cred-confirmed="deleteCred"></connected-table>
  </div>
</template>

<script>
import ConnectForm from "@/components/ConnectForm";
import ConnectedTable from "@/components/ConnectedTable";
import {getCredentials, deleteCredential} from "@/api/credential";

export default {
  name: "ConnectView",
  data() {
    return {
      credentialList: []
    }
  },
  components: {
    ConnectForm,
    ConnectedTable,
  },
  methods: {
    setCredentialList(data) {
      this.credentialList = data.map(cred => ({
        credId: cred.id,
        exchangeNameZh: cred['exchange']['name_zh'],
        note: cred.note,
        apiKey: cred['api_key'],
        secret: cred['secret'],
        createdAt: cred['created_at'],
      }))
    },
    async getCredentialList() {
      try {
        const credentialsRes = await getCredentials()
        this.setCredentialList(credentialsRes.data)
      } catch (error) {
        if (error.response) {
          this.$bvToast.toast('无法获取交易所凭据', {
            title: '无法获取交易所凭据',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '无法获取交易所凭据',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        }
      }
    },
    async deleteCred({credId}) {
      try {
        await deleteCredential(credId)
        await this.getCredentialList()
      } catch (error) {
        if (error.response) {
          this.$bvToast.toast('删除失败', {
            title: '删除失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '删除失败',
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
    await this.getCredentialList()
  },
}
</script>

