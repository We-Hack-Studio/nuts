<template>
  <div class="mx-sm-2 mx-md-3">
    <b-row>
      <b-col md="8">
        <h3>{{ strategy.name }}</h3>
        <div class="mt-2 text-muted small">{{ strategy.brief }}</div>
        <div class="mt-3">{{ strategy.description }}</div>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import {getStrategy} from '@/api/strategy';

export default {
  name: "StrategyDetailView",
  data() {
    return {
      strategy: {}
    }
  },
  methods: {
    async getStrategyDetail() {
      try {
        const strategyRes = await getStrategy(this.$route.params.id);
        this.strategy = {
          name: strategyRes.data.name,
          brief: strategyRes.data.brief,
          description: strategyRes.data.description,
        };
      } catch (error) {
        if (error.response) {
          this.$bvToast.toast('无法获取策略详情', {
            title: '无法获取策略详情',
            autoHideDelay: 2000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false,
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '无法获取策略详情',
            autoHideDelay: 2000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false,
          });
        }
      }
    },
  },
  mounted() {
    this.getStrategyDetail()
  }
}
</script>

<style scoped>

</style>