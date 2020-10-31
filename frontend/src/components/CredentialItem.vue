<template>
  <b-card>
    <div class="justify-content-between d-flex mb-2">
      <span class="font-weight-bold">{{ credential.note }}</span>
      <span class="action-buttons">
        <a href="#" class="mr-2" @click="edit"><b-icon-pencil-square></b-icon-pencil-square></a>
        <a href="#" class="text-danger" @click="showPrompt(credential.credId)">
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
</template>

<script>
export default {
  name: 'CredentialItem',
  props: {
    credential: Object,
  },
  methods: {
    edit() {
      let initial = {
        credentialId: this.credential.credId,
        exchange: this.credential.exchangeId,
        note: this.credential.note,
        testNet: this.credential.testNet,
      }
      this.$emit("edit", {initial: initial})
    },
    showPrompt(credId) {
      this.$bvModal.msgBoxConfirm('删除交易所凭据将连带删除关联的机器人，这可能导致交易异常。', {
        title: '确认删除？',
        size: 'sm',
        buttonSize: 'sm',
        okVariant: 'danger',
        okTitle: '确认',
        cancelTitle: '取消',
        footerClass: 'p-2',
        hideHeaderClose: false,
        centered: true,
      })
          .then(value => {
            if (!value) {
              return
            }
            this.$emit("delete-confirmed", {credId: credId})
          })
          .catch(err => {
            console.log(err);
            // An error occurred
          })
    }
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.credential {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
