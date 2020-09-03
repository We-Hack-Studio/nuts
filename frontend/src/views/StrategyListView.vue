<template>
  <b-row>
    <b-col md="6">
      <strategy-item
          v-for="strategy in strategyList"
          :strategy="strategy"
          :key="strategy.id"
          class="mt-3">
      </strategy-item>
    </b-col>
  </b-row>
</template>

<script>
import StrategyItem from "../components/StrategyItem"
import formatterMixin from "@/mixins/formatter"
import {getStrategies} from "@/api"

export default {
  name: "strategy-list",
  components: {
    StrategyItem
  },
  mixins: [formatterMixin],
  data() {
    return {
      strategyList: []
    }
  },
  methods: {
    setStrategyList(data) {
      this.strategyList = data.map(strategy => ({
        id: strategy.id,
        name: strategy.name,
        description: strategy.description,
      }))
    },
    async getStrategyList() {
      try {
        const strategiesRes = await getStrategies()
        const result = this.formatter.deserialize(strategiesRes.data)
        this.setStrategyList(result.data)
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
    }
  },
  mounted() {
    this.getStrategyList()
  },
}
</script>

<style scoped>

</style>