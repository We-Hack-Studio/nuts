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
import formatterMixin from "@/mixins/formatter"

export default {
  data() {
    return {
      credentialOptions: [],
      strategyOptions: [],
    }
  },
  mixins: [formatterMixin],
  components: {
    RobotCreateForm,
  },
  methods: {
    async getCredentialOptions() {
      try {
        const credentialsRes = await getCredentials()
        const result = this.formatter.deserialize(credentialsRes.data)
        this.setCredentialOptions(result.data)
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
    setCredentialOptions(data) {
      this.credentialOptions = data.map(cred => ({value: cred.id, text: `${cred.exchange.data.name} - ${cred.note}`}))
    },
    async getStrategyOptions() {
      try {
        const strategiesRes = await getStrategies()
        const result = this.formatter.deserialize(strategiesRes.data)
        this.setStrategyOptions(result.data)
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
    setStrategyOptions(data) {
      this.strategyOptions = data.map(st => ({value: st.id, text: st.name}))
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
