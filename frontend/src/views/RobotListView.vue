<template>
  <div class="robot-list-view">
    <b-row class="row">
      <b-col md="6" xl="4" offset-md="3" offset-xl="4" v-for="robot in robotList" :key="robot.robotId">
        <robot-list-item :robot="robot" @refresh="refreshList"></robot-list-item>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import RobotListItem from '../components/RobotListItem';
import {getRobots} from '@/api';

export default {
  name: 'robot-list',
  components: {
    RobotListItem,
  },
  data() {
    return {
      robotList: [],
      timer: '', // 定时器id
    };
  },
  methods: {
    refreshList() {
      this.getRobotList();
    },
    setRobotList(data) {
      this.robotList = data.map(robot => ({
        robotId: robot.id,
        name: robot.name,
        pair: robot.pair,
        targetCurrency: robot.target_currency,
        enabled: robot.enabled,
        startTime: robot['start_time'],
        pingTime: robot['ping_time'],
        createdAt: robot['created_at'],
        durationDisplay: robot['duration_display'],
        strategyName: robot["strategy_name"],
        exchangeNameZh: robot['exchange']['name_zh'],
        exchangeName: robot.exchange.name,
        profitRatioPtg: robot['asset_record']['total_pnl_rel_ptg'],
        profitRatioPtg24h: robot['asset_record']['total_pnl_rel_ptg_24h'],
        profit24h: robot['asset_record']['total_pnl_abs_24h'],
        profit: robot['asset_record']['total_pnl_abs'],
        principal: robot['asset_record']['total_principal'],
        balance: robot['asset_record']['total_balance'],
      }));
    },
    async getRobotList() {
      try {
        const robotsRes = await getRobots();
        console.log(robotsRes)
        this.setRobotList(robotsRes.data);
      } catch (error) {
        if (error.response) {
          this.$bvToast.toast('无法获取机器人列表数据', {
            title: '无法获取机器人列表数据',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false,
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '无法获取机器人列表数据',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false,
          });
        }
      }
    },
  },
  mounted() {
    this.getRobotList();
    this.timer = setInterval(this.getRobotList, 10 * 1000);
  },
  beforeDestroy() {
    clearInterval(this.timer);
  },
};
</script>

<style scoped lang="scss">
.robot-list-view {
  width: 100%;

  .row {
    margin: 0;
  }
}
</style>
