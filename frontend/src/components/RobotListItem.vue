<template>
  <b-card class="mb-4">
    <div class="d-flex">
      <span class="mr-1 text-success"><b-icon icon="circle-fill" animation="throb"></b-icon></span>
      <a href="#" class="font-weight-bold">{{robot.name}}</a>
      <span class="ml-auto">
        <a href="#" class="mr-2">
          <b-icon-pencil-square></b-icon-pencil-square>
        </a>
        <a href="#" class="text-danger">
          <b-icon-trash></b-icon-trash>
        </a>
      </span>
    </div>
    <div class="d-flex justify-content-between mt-2">
      <span><span class="small text-muted">收益率</span><br><span
              class="text-success h5">{{robot.profitRatioPtg}}</span></span>
      <span><span class="small text-muted">收益额</span><br><span class="text-success">{{robot.profit}}</span></span>
      <span><span class="small text-muted">本金</span><br><span class="">{{robot.principal}}</span></span>
      <span><span class="small text-muted">余额</span><br><span class="">{{robot.balance}}</span></span>
    </div>
    <div class="text-muted mt-2">
      <span class="mr-2">{{robot.exchangeNameZh}}</span>
      <span>{{robot.pair}}</span>
      <span class="float-right">{{robot.durationDisplay}}</span>
    </div>
    <hr>
    <div class="small">
      <span class="mr-1 text-muted">较前日</span>
      <span class="text-success mr-1"><b-icon-caret-up-fill></b-icon-caret-up-fill> 1.5%</span>
      <span class="text-success">4U</span>
      <span class="float-right">网格策略</span>
    </div>
  </b-card>
</template>

<script>
    export default {
        name: 'RobotListCard',
        props: {
            robot: Object,
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h3 {
    margin: 40px 0 0;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }
</style>
