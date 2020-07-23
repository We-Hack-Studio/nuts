<template>
  <div>
    <b-table small striped hover :items="credentialList" :fields="fields" responsive="sm">
      <template v-slot:cell(action)="data">
        <b-icon-trash v-b-modal="'delete-confirm-model'"
                      @click="showMsgBox(data.item.credId, data.index)"></b-icon-trash>
      </template>
    </b-table>
  </div>
</template>

<script>
    import moment from 'moment'

    export default {
        name: 'ConnectedTable',
        props: {
            credentialList: Array
        },
        data() {
            return {
                fields: [
                    {
                        key: 'exchangeNameZh',
                        label: '交易所'
                    },
                    {
                        key: 'note',
                        label: '备注'
                    },
                    {
                        key: 'apiKeyMasked',
                        label: 'API Key'
                    },
                    {
                        key: 'secretMasked',
                        label: 'Secret'
                    },
                    {
                        key: 'createdAt',
                        label: '创建时间',
                        formatter: (value) => {
                            return moment(value).format('YYYY-MM-DD HH:mm:ss')
                        }
                    },
                    {
                        key: 'action',
                        label: '操作'
                    }
                ],
            }
        },
        methods: {
            showMsgBox(credId, index) {
                this.$bvModal.msgBoxConfirm('删除交易所凭证将同时清除关联的机器人。', {
                    title: '确认删除？',
                    size: 'sm',
                    buttonSize: 'sm',
                    okVariant: 'danger',
                    okTitle: '确认',
                    cancelTitle: '取消',
                    footerClass: 'p-2',
                    hideHeaderClose: false,
                    centered: true
                })
                    .then(value => {
                        if (!value) {
                            return
                        }
                        this.$emit("delete-cred-confirmed", {credId: credId, index: index})
                    })
                    .catch(err => {
                        console.log(err);
                        // An error occurred
                    })
            }
        }
    }
</script>