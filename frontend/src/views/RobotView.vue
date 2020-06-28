<template>
  <b-row>
    <b-col md="5">
      <robot-log :robotEnabled="robotEnabled" :robot-log-list="robotLogList" :robotStreamKey="robotStreamKey"
                 v-if="robotStreamKey!==''"
                 @robot-switch="robotEnabled=!robotEnabled"></robot-log>
    </b-col>
    <b-col md="7">
      <grid-table :grid-list="gridList" @grids-created="loadGridTable" @grids-cleared="gridList=[]"
                  @refresh-grids="loadGridTable"></grid-table>
    </b-col>
  </b-row>
</template>

<script>
    import RobotLog from "../components/RobotLog";
    import GridTable from "../components/GridTable";
    import {getRobot} from "../api";
    import {getGridList} from "../api";

    export default {
        name: "Ranking",
        data() {
            return {
                robotEnabled: false,
                robotStreamKey: '',
                robotLogList: [],
                gridList: []
            }
        },
        components: {
            RobotLog,
            GridTable,
        },
        methods: {
            subscribe() {
                let vm = this
                let robotId = vm.$route.params.id
                let robotSocket = new WebSocket(
                    window.conf.robotStreamWsUri.replace('{pk}', robotId) + '?stream_key=' + vm.robotStreamKey
                );

                robotSocket.onmessage = function (e) {
                    let data = JSON.parse(e.data);
                    if (data.topic === 'log') {
                        vm.robotLogList.push(data);
                        if (vm.robotLogList.length > 100) {
                            vm.robotLogList.shift()
                        }
                    } else if (data.topic === 'grid') {
                        vm.setGridList(data.data)
                    }
                };

                robotSocket.onclose = function () {
                    console.error('Robot socket closed unexpectedly');
                };

                robotSocket.onopen = function () {
                    console.info("Websocket opened!");
                };
            },
            setGridList(data) {
                this.gridList = data.map(grid => ({
                    gridId: grid.id,
                    gridIndex: grid.index,
                    entryPrice: grid['entry_price'],
                    exitPrice: grid['exit_price'],
                    entryQty: grid['entry_qty'],
                    filledQty: grid['filled_qty'],
                    holding: grid.holding,
                }))
            },
            loadGridTable() {
                getGridList(this.$route.params.id).then(response => {
                    this.setGridList(response.data)
                }).catch(err => {
                    console.log(err.data);
                })
            },
        },
        mounted() {
            getRobot(this.$route.params.id).then(response => {
                this.robotEnabled = response.data.enabled
                this.robotStreamKey = response.data['stream_key']
                this.subscribe()
            }).catch(err => {
                this.$bvToast.toast(`获取机器人配置失败，错误信息： ${err.data}`, {
                    title: '数据获取失败',
                    autoHideDelay: 3000,
                    toaster: 'b-toaster-top-center',
                    variant: 'danger',
                    appendToast: false
                });
            })
            this.loadGridTable()
        },
    }
</script>

<style scoped>

</style>
