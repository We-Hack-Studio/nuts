<template>
  <div>
    <b-row>
      <b-col md="8">
        <connect-form @credential-added="updateCredentialList"></connect-form>
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
    import ConnectForm from "../components/ConnectForm";
    import ConnectedTable from "../components/ConnectedTable";
    import {getCredentialList, deleteCredential} from "../api";

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
                    exchangeNameZh: cred['exchange_info']['name_zh'],
                    note: cred.note,
                    apiKeyMasked: cred['api_key_masked'],
                    secretMasked: cred['secret_masked'],
                    createdAt: cred['created_at'],
                }))
            },
            updateCredentialList(cred) {
                this.credentialList.splice(0, 0, cred)
                this.$bvToast.toast('交易所接入成功！', {
                    title: '成功',
                    autoHideDelay: 3000,
                    toaster: 'b-toaster-top-center',
                    variant: 'success',
                    appendToast: false
                });
            },
            deleteCred({credId, index}) {
                deleteCredential(credId).then(() => {
                    this.credentialList.splice(index, 1)
                }).catch(err => {
                    console.log(err.data);
                })
            }
        },
        mounted() {
            getCredentialList().then(response => {
                this.setCredentialList(response.data)
            }).catch(err => {
                console.log(err.data);
            })
        },
    }
</script>

<style scoped>

</style>