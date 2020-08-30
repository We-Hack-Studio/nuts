<template>
  <b-row>
    <b-col md="6" offset-md="3">
      <robot-create-form
          :credential-options="credentialOptions"
          :strategy-template-options="strategyOptions">
      </robot-create-form>
    </b-col>
  </b-row>
</template>

<script>
import RobotCreateForm from "../components/RobotCreateForm";
import {getCredentials, getStrategies} from "@/api";

export default {
  data() {
    return {
      credentialOptions: [],
      strategyOptions: [],
    }
  },
  components: {
    RobotCreateForm,
  },
  methods: {
    setCredentialOptions(data) {
      this.credentialOptions = data.map(cred => ({value: cred.id, text: `${cred.exchange.name} - ${cred.note}`}))
    },
    setStrategyOptions(data) {
      this.strategyOptions = data.map(st => ({value: st.id, text: st.name}))
    },
  },
  mounted() {
    getCredentials().then(response => {
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
    getStrategies().then(response => {
      this.setStrategyOptions(response.data.results)
    }).catch(err => {
      this.$bvToast.toast(`无法获取策略，错误信息：${err.data || '未知错误'}`, {
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
