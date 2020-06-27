<template>
  <div>
    <div class="d-flex justify-content-between">
      <span>{{robot.robotId}}</span>
      <span>{{robot.exchangeNameZh}}</span>
      <span>{{robot.pair}}</span>
      <span>{{robot.durationDisplay || '0天0小时'}}</span>
      <span>{{robot.profitRatioPtg || '0.00%'}}</span>
      <span><b-icon-chevron-right></b-icon-chevron-right></span>
    </div>
  </div>
</template>

<script>
    export default {
        name: 'RobotItem',
        props: {
            robot: Object
        }
    }
</script>

<style scoped>
</style>
