<template>
  <b-row>
    <b-col sm="12" md="6" lg="4" v-for="credential in credentialList" :key="credential.credId">
      <b-card class="mt-4">
        <div class="justify-content-between d-flex mb-2">
          <span class="font-weight-bold">{{ credential.note }}</span>
          <span class="action-buttons">
              <router-link to="/" class="mr-2">
                <b-icon-pencil-square></b-icon-pencil-square>
              </router-link>
              <a href="#" class="text-danger" @click="showMsgBox">
                <b-icon-trash></b-icon-trash>
              </a>
            </span>
        </div>
        <div class="credential">
          <b-icon icon="lock" variant="success" class="mr-2"></b-icon>
          <span class="text-success">API Key：</span>
          <span class="text-muted">{{ credential.apiKey }}</span>
        </div>
        <div class="credential">
          <b-icon icon="lock" variant="success" class="mr-2"></b-icon>
          <span class="text-success">Secret：</span>
          <span class="text-muted">{{ credential.secret }}</span>
        </div>
        <div class="credential">
          <b-icon icon="lock" variant="success" class="mr-2"></b-icon>
          <span class="text-success">Passphrase：</span>
          <span class="text-muted">{{ credential.passphrase || '-' }}</span>
        </div>
      </b-card>
    </b-col>
  </b-row>
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

<style scoped>
.credential {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>