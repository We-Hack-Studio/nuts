<template>
  <div v-if="orderStore">
    <div
        :key="index"
        v-for="(order, index) in orderStore.orders"
    >
      <order-item :order="order"></order-item>
    </div>
  </div>
</template>

<script>
import OrderItem from "@/components/robot-console/OrderItem";

export default {
  name: 'Order',
  props: ['orderStore'],
  components: {OrderItem}
};
</script>

<style></style>
