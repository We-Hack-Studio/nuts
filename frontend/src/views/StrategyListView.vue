<template>
  <div class="mx-sm-2 mx-md-3">
    <div class="mb-3">
      <router-link :to="{name: 'strategy-add'}">
        <b-button variant="primary">
          <b-icon icon="plus" aria-hidden="true"></b-icon>
          新增策略
        </b-button>
      </router-link>
    </div>
    <b-row>
      <b-col sm="12" md="6" lg="4" v-for="strategy in strategyList" :key="strategy.id" class="mb-3">
        <strategy-item
            :strategy="strategy"
            class="strategy-item">
        </strategy-item>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import StrategyItem from "../components/StrategyItem"
import {getStrategies} from "@/api"

export default {
  name: "strategy-list",
  components: {
    StrategyItem
  },
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
        console.log(strategiesRes)
        this.setStrategyList(strategiesRes.data.results)
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

<style lang="scss" scoped>
.strategy-item {
  height: 100%;
}
</style>