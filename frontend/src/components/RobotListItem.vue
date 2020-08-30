<template>
  <b-card class="mb-4 card">
    <div class="d-flex align-items-center">
      <span :class="['mr-1','d-inline-flex', robotStatusClass]">
        <b-icon icon="circle-fill" font-scale="0.6" :animation="robotStatusAnimation"></b-icon>
      </span>
      <router-link :to="{name: 'robot',params: {id:robot.robotId}}" class="font-weight-bold text-body">
        {{ robot.name }}
      </router-link>
      <span class="ml-auto action-buttons">
        <router-link :to="{name: 'robot-update',params: {id:robot.robotId}}" class="mr-2">
          <b-icon-pencil-square></b-icon-pencil-square>
        </router-link>
        <a href="#" class="text-danger">
          <b-icon-trash></b-icon-trash>
        </a>
      </span>
    </div>
    <div class="d-flex justify-content-between mt-2">
      <span><span class="small text-muted">收益率</span><br><span
          :class="[profitColorClass, 'h5']">{{ robot.profitRatioPtg }}</span></span>
      <span><span class="small text-muted">收益额</span><br><span
          :class="profitColorClass">{{ robot.profit|roundByCurrency(robot.targetCurrency) }}
          <span class="font-weight-light"> {{ robot.targetCurrency }}</span>
        </span></span>
      <span><span class="small text-muted">本金</span><br><span
          class="">{{ robot.principal|roundByCurrency(robot.targetCurrency) }}
          <span class="font-weight-light"> {{ robot.targetCurrency }}</span>
        </span></span>
      <span><span class="small text-muted">余额</span><br><span
          class="">{{ robot.balance |roundByCurrency(robot.targetCurrency) }}
          <span class="font-weight-light"> {{ robot.targetCurrency }}</span>
        </span></span>
    </div>
    <div class="text-muted mt-2">
      <span class="mr-2">{{ robot.exchangeNameZh }}</span>
      <span>{{ robot.pair }}</span>
      <span class="float-right">{{ robot.durationDisplay }}</span>
    </div>
    <hr>
    <div class="small">
      <span class="mr-1 text-muted">较前日</span>
      <span :class="[profit24hColorClass, 'mr-1']">
        <b-icon-caret-up-fill v-if="robot.profit24h > 0"></b-icon-caret-up-fill>
        <b-icon-caret-down-fill v-if="robot.profit24h < 0"></b-icon-caret-down-fill>
        {{ robot.profitRatioPtg24h }}
      </span>
      <span :class="profit24hColorClass">{{ robot.profit24h|roundByCurrency(robot.targetCurrency) }}
        <span class="font-weight-light"> {{ robot.targetCurrency }}</span>
      </span>
      <span class="float-right">网格策略</span>
    </div>
  </b-card>
</template>

<script>
import moment from 'moment'

export default {
  name: 'RobotListItem',
  props: {
    robot: Object,
  },
  computed: {
    robotStatusClass() {
      return moment().diff(this.robot.pingTime, 'seconds') < 60 ? 'text-success' : 'text-danger';
    },
    robotStatusAnimation() {
      return this.robotStatusClass === 'text-danger' ? '' : 'throb'
    },
    profitColorClass() {
      return this.robot.profit > 0 ? 'text-success' : this.robot.profit < 0 ? 'text-danger' : ''
    },
    profit24hColorClass() {
      return this.robot.profit24h > 0 ? 'text-success' : this.robot.profit24h < 0 ? 'text-danger' : ''
    }
  },
  filters: {
    roundByCurrency(value, currency) {
      switch (currency) {
        case "BTC":
          return value.toFixed(4)
        case "USDT":
          return value.toFixed(2)
        default:
          return value
      }
    }
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


.action-buttons {
  display: none;
}

.card:hover .action-buttons {
  display: inline-block;
}
</style>