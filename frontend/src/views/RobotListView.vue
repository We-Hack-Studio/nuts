<template>
  <b-row>
    <b-col md="4" v-for="robot in robotList" :key="robot.robotId">
      <robot-list-item :robot="robot"></robot-list-item>
    </b-col>
  </b-row>

</template>

<script>
import RobotListItem from "../components/RobotListItem";
import {getRobots} from "../api";

export default {
  name: "robot-list",
  components: {
    RobotListItem
  },
  data() {
    return {
      robotList: [],
      timer: '', // 定时器id
    }
  },
  methods: {
    setRobotList(data) {
      this.robotList = data.map(r => ({
        robotId: r.id,
        exchangeNameZh: r.exchange['name_zh'],
        name: r.name,
        pair: r.pair,
        targetCurrency: r.target_currency,
        enable: r.enable,
        pingTime: r['ping_time'],
        startTime: r['start_time'],
        durationDisplay: r['duration_display'],
        profitRatioPtg: r['asset_record']['total_pnl_rel_ptg'],
        profitRatioPtg24h: r['asset_record']['total_pnl_rel_ptg_24h'],
        profit24h: r['asset_record']['total_pnl_abs_24h'],
        profit: r['asset_record']['total_pnl_abs'],
        principal: r['asset_record']['total_principal'],
        balance: r['asset_record']['total_balance'],
        createdAt: r['created_at'],
      }))
    },
    loadRobotList() {
      getRobots().then(response => {
        this.setRobotList(response.data)
      }).catch(err => {
        console.log(err.data);
      })
    }
  },
  mounted() {
    this.loadRobotList()
    this.timer = setInterval(this.loadRobotList, 10 * 1000)
  },
  beforeDestroy() {
    clearInterval(this.timer)
  },
}
</script>

<style scoped>

</style>