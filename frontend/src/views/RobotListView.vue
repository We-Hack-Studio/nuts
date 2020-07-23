<template>
  <b-row>
    <b-col md="4" v-for="robot in robotList" :key="robot.robotId">
      <robot-list-item :robot="robot"></robot-list-item>
    </b-col>
  </b-row>

</template>

<script>
    import RobotListItem from "../components/RobotListItem";
    import {getRobotList} from "../api";

    export default {
        name: "robot-list",
        components: {
            RobotListItem
        },
        data() {
            return {
                robotList: []
            }
        },
        methods: {
            setRobotList(data) {
                this.robotList = data.map(r => ({
                    robotId: r.id,
                    exchangeNameZh: r.exchange['name_zh'],
                    name: r.name,
                    pair: r.pair,
                    marginCurrency: r.margin_currency,
                    enable: r.enable,
                    pingTime: r['ping_time'],
                    startTime: r['start_time'],
                    durationDisplay: r['duration_display'],
                    profitRatioPtg: r['profit_ratio_ptg'],
                    profit: r.profit,
                    principal: r.principal,
                    balance: r.balance,
                    createdAt: r['created_at'],
                }))
            },
            loadRobotList() {
                getRobotList().then(response => {
                    this.setRobotList(response.data)
                }).catch(err => {
                    console.log(err.data);
                })
            }
        },
        mounted() {
            this.loadRobotList()
        },
    }
</script>

<style scoped>

</style>