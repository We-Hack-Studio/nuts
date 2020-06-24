<template>
  <div>
    <b-card header-tag="header" footer-tag="footer">
      <template v-slot:header>
        <div class="d-flex justify-content-between"><span>日志监控</span>
          <toggle-button :value="robotEnabled" :sync="true" :disabled="robotSwitchDisabled"
                         @change="handleRobotSwitch"
                         :labels="{checked: 'On', unchecked: 'Off'}"/>
        </div>
      </template>
      <p v-for="log in robotLogList" :key="log.timestamp">{{log.timestamp}} {{log.msg}}</p>
    </b-card>
  </div>
</template>

<script>
    import {updateRobot} from "../api";

    export default {
        name: 'RobotLog',
        props: {
            robotEnabled: Boolean,
            robotStreamKey: String,
        },
        data() {
            return {
                robotSwitchDisabled: false,
                robotLogList: []
            }
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
                    vm.robotLogList.push(data);
                };

                robotSocket.onclose = function () {
                    console.error('Robot socket closed unexpectedly');
                };

                robotSocket.onopen = function () {
                    console.info("Websocket opened!");
                    // let message = JSON.stringify({
                    //     'cmd': "sub",
                    //     'params': ['robot.' + robotId],
                    //     "id": "fisher"
                    // })
                    // robotSocket.send(message);
                };
            },
            handleRobotSwitch({value}) {
                this.robotSwitchDisabled = true
                updateRobot(this.$route.params.id, {"enabled": value}).then(() => {
                    this.robotSwitchDisabled = false
                    this.$emit("robot-switch")
                }).catch(err => {
                    console.log(err.data);
                })
            }
        },
        mounted() {
            // 组件创建完后获取数据，
            // 此时 data 已经被 observed 了
            this.subscribe()
        },
    }
</script>

<style scoped>
</style>
