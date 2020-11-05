<template>
  <b-card header-tag="header">
    <template v-slot:header>
      <div class="d-flex justify-content-between align-items-center">
        <span class="h6 m-0">机器人</span>
      </div>
    </template>
    <div v-if="overviewData">
      <div class="mb-1">ID：{{ overviewData.RobotId }}</div>
      <div class="mb-1">名称：{{ overviewData.name }}</div>
      <div class="mb-1">市场类型：{{ overviewData.marketTypeDisplay }}</div>
      <div class="mb-1">交易对：{{ overviewData.pair }}</div>
      <div class="mb-1">基础币种：{{ overviewData.baseCurrency }}</div>
      <div class="mb-1">计价币种：{{ overviewData.quoteCurrency }}</div>
      <div class="mb-1">策略：{{ overviewData.strategyName }}</div>
      <div class="mb-1">目标币种：{{ overviewData.targetCurrency }}</div>
      <div class="mb-1">运行时间：{{ overviewData.durationDisplay }}</div>
      <div class="mb-1">本金：{{ overviewData.totalPrincipal }}</div>
      <div class="mb-1">余额：{{ overviewData.totalBalance }}</div>
      <div class="mb-1">收益额：{{ overviewData.totalPnlAbs }}</div>
      <div class="mb-1">收益率：{{ overviewData.totalPnlRelPtg }}</div>
      <div class="mb-1">较前日：10(10.2%)</div>
    </div>
  </b-card>
</template>

<script>
export default {
  props: {
    overviewData: Object
  },
  data() {
    return {};
  },
  methods: {},
};
</script>
