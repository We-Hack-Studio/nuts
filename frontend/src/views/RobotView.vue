<template>
  <b-row>
    <b-col md="4">
      <robot-log :robotEnabled="robotEnabled" :robotStreamKey="robotStreamKey" v-if="robotStreamKey!==''"
                 @robot-switch="robotEnabled=!robotEnabled"></robot-log>
    </b-col>
    <b-col md="8">
      <grid-table></grid-table>
    </b-col>
  </b-row>
</template>

<script>
    import RobotLog from "../components/RobotLog";
    import GridTable from "../components/GridTable";
    import {getRobot} from "../api";

    export default {
        name: "Ranking",
        data() {
            return {
                robotEnabled: false,
                robotStreamKey: '',
            }
        },
        components: {
            RobotLog,
            GridTable,
        },
        methods: {},
        mounted() {
            getRobot(this.$route.params.id).then(response => {
                this.robotEnabled = response.data.enabled
                this.robotStreamKey = response.data['stream_key']
            }).catch(err => {
                this.$bvToast.toast(`获取机器人配置失败，错误信息： ${err.data}`, {
                    title: '数据获取失败',
                    autoHideDelay: 3000,
                    toaster: 'b-toaster-top-center',
                    variant: 'danger',
                    appendToast: false
                });
            })
        },
    }
</script>

<style scoped>

</style>