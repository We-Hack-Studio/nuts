<template>
  <div class="justify-content-between d-flex">
    <div>
      <div class="small text-secondary">持仓数量</div>
      <div :class="getProfitColorClass(position)">{{ position.qty * position.side }}</div>
    </div>
    <div>
      <div class="small text-secondary">均价</div>
      <div>{{ position.avgPrice }}</div>
    </div>
    <div>
      <div class="small text-secondary">强平价</div>
      <div>{{ position.liqPrice }}</div>
    </div>
    <div>
      <div class="small text-secondary">未实现盈亏</div>
      <div :class="getUplColor(position)">{{ position.unrealizedPnl }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PositionItem',
  props: {
    position: Object
  },
  methods: {
    getProfitColorClass(position) {
      return position.side > 0 ? 'text-success' : 'text-danger';
    },
    getUplColor(position) {
      return position.unrealizedPnl > 0 ? 'text-success' : 'text-danger';
    },
  },
};
</script>
<style scoped></style>
