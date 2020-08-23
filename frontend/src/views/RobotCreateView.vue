<template>
  <b-row>
    <b-col md="6" offset-md="3">
      <robot-create-form
          :credential-options="credentialOptions"
          :strategy-template-options="strategyTemplateOptions">
      </robot-create-form>
    </b-col>
  </b-row>
</template>

<script>
import RobotCreateForm from "../components/RobotCreateForm";
import {getCredentialList, getStrategyTemplateList} from "@/api";

export default {
  data() {
    return {
      credentialOptions: [],
      strategyTemplateOptions: [],
    }
  },
  components: {
    RobotCreateForm,
  },
  methods: {
    setCredentialOptions(data) {
      this.credentialOptions = data.map(cred => ({value: cred.id, text: `${cred.exchange.name} - ${cred.note}`}))
    },
    setStrategyTemplateOptions(data) {
      this.strategyTemplateOptions = data.map(st => ({value: st.id, text: st.name}))
    },
  },
  mounted() {
    getCredentialList().then(response => {
      this.setCredentialOptions(response.data)
    }).catch(err => {
      this.$bvToast.toast(`无法获取交易所凭证，错误信息：${err.data || '未知错误'}`, {
        title: '数据获取失败',
        autoHideDelay: 3000,
        toaster: 'b-toaster-top-right',
        variant: 'danger',
        appendToast: false
      });
    });
    getStrategyTemplateList().then(response => {
      this.setStrategyTemplateOptions(response.data.results)
    }).catch(err => {
      this.$bvToast.toast(`无法获取策略模板，错误信息：${err.data || '未知错误'}`, {
        title: '数据获取失败',
        autoHideDelay: 3000,
        toaster: 'b-toaster-top-right',
        variant: 'danger',
        appendToast: false
      });
    });
  },
}
</script>

<style scoped>
</style>
