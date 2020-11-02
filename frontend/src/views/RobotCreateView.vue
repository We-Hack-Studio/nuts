<template>
  <b-container fluid="">
    <robot-form
        :credential-options="credentialOptions"
        :strategy-options="strategyOptions">
    </robot-form>
  </b-container>
</template>

<script>
import RobotForm from "../components/RobotForm";
import {getCredentials, getStrategies} from "@/api";

export default {
  data() {
    return {
      credentialOptions: [],
      strategyOptions: [],
    }
  },
  components: {
    RobotForm,
  },
  methods: {
    async getCredentialOptions() {
      try {
        const credentialsRes = await getCredentials()
        this.credentialOptions = credentialsRes.data.map(cred => ({
          value: cred.id,
          text: `${cred.exchange.name} - ${cred.note}`
        }))
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
    async getStrategyOptions() {
      try {
        const strategiesRes = await getStrategies()
        this.strategyOptions = strategiesRes.data.results.map(s => ({value: s.id, text: s.name}))
      } catch (error) {
        if (error.response) {
          this.$bvToast.toast('无法获取策略列表数据', {
            title: '无法获取策略列表数据',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '无法获取策略列表数据',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        }
      }
    },
  },
  async mounted() {
    await this.getCredentialOptions()
    await this.getStrategyOptions()
  },
}
</script>

<style scoped>
</style>
