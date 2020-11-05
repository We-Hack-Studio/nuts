<template>
  <div v-if="positionStore">
    <div
        :key="index"
        v-for="(position, index) in positionStore.positions"
    >
      <position-item :position="position"/>
    </div>
  </div>
</template>

<script>
import PositionItem from "@/components/robot-console/PositionItem";

export default {
  name: 'Position',
  props: {positionStore: Object},
  components: {PositionItem},
  mounted() {
    console.log(this.positionStore)
  }
};
</script>

<style></style>
