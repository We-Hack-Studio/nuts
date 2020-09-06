<template>
  <b-row>
    <b-col md="6" xl="4" offset-md="3" offset-xl="4" v-for="robot in robotList" :key="robot.robotId">
      <robot-list-item :robot="robot" @refresh="refreshList"></robot-list-item>
    </b-col>
  </b-row>
</template>

<script>
import RobotListItem from '../components/RobotListItem';
import { getRobots } from '@/api';
import formatterMixin from '@/mixins/formatter';

export default {
  name: 'robot-list',
  components: {
    RobotListItem,
  },
  mixins: [formatterMixin],
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
        exchangeNameZh: robot['exchange']['data']['name_zh'],
        profitRatioPtg: robot['asset_record']['data']['total_pnl_rel_ptg'],
        profitRatioPtg24h: robot['asset_record']['data']['total_pnl_rel_ptg_24h'],
        profit24h: robot['asset_record']['data']['total_pnl_abs_24h'],
        profit: robot['asset_record']['data']['total_pnl_abs'],
        principal: robot['asset_record']['data']['total_principal'],
        balance: robot['asset_record']['data']['total_balance'],
      }));
    },
    async getRobotList() {
      try {
        const robotsRes = await getRobots();
        const result = this.formatter.deserialize(robotsRes.data);
        this.setRobotList(result.data);
        console.log(result);
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

<style scoped></style>
