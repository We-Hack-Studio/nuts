<template>
  <b-row>
    <b-col md="8">
      <b-list-group>
        <b-list-group-item v-for="robot in robotList" :key="robot.robotId" :to="robot.robotId + ''"
                           class="flex-column align-items-start">
          <robot-item :robot="robot"></robot-item>
        </b-list-group-item>
      </b-list-group>
    </b-col>
    <b-col md="4">
      <robot-form @robot-created="loadRobotList"></robot-form>
    </b-col>
  </b-row>
</template>

<script>
    import RobotItem from "../components/RobotItem";
    import RobotForm from "../components/RobotForm";
    import {getRobotList} from "../api";

    export default {
        name: "Ranking",
        data() {
            return {
                robotList: []
            }
        },
        components: {
            RobotItem,
            RobotForm,
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