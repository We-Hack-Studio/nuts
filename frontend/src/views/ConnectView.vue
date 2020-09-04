<template>
  <div>
    <b-row>
      <b-col md="8">
        <connect-form @credential-added="getCredentialList"></connect-form>
      </b-col>
      <b-col md="4">
      </b-col>
    </b-row>
    <b-row class="mt-4">
      <b-col md="8">
        <connected-table :credential-list="credentialList" @delete-cred-confirmed="deleteCred"></connected-table>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import ConnectForm from "@/components/ConnectForm";
import ConnectedTable from "@/components/ConnectedTable";
import {getCredentials, deleteCredentialsId} from "@/api";
import formatterMixin from "@/mixins/formatter"

export default {
  name: "ConnectView",
  mixins: [formatterMixin],
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
        exchangeNameZh: cred['exchange']["data"]['name_zh'],
        note: cred.note,
        apiKeyMasked: cred['api_key_masked'],
        secretMasked: cred['secret_masked'],
        createdAt: cred['created_at'],
      }))
    },
    async getCredentialList() {
      try {
        const credentialsRes = await getCredentials()
        const result = this.formatter.deserialize(credentialsRes.data)
        this.setCredentialList(result.data)
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
    async deleteCred({credId, index}) {
      try {
        await deleteCredentialsId(credId)
        this.credentialList.splice(index, 1)
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

<style scoped>

</style>