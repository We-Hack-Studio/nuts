<template>
  <div>
    <div>Robot Stream Key:</div>
    <div class="d-flex justify-content-between" v-if="hideStreamKey">
      <span class="small">{{maskedRobotStreamKey}}</span>
      <b-icon-eye @click="hideStreamKey=!hideStreamKey"></b-icon-eye>
    </div>
    <div class="d-flex justify-content-between" v-if="!hideStreamKey">
      <span class="small">{{robotStreamKey}}</span>
      <b-icon-eye-slash @click="hideStreamKey=!hideStreamKey"></b-icon-eye-slash>
    </div>
    <b-card class="mt-3" header-tag="header" footer-tag="footer">
      <template v-slot:header>
        <div class="d-flex justify-content-between"><span>日志监控</span>
          <toggle-button :value="robotEnabled" :sync="true" :disabled="robotSwitchDisabled"
                         @change="handleRobotSwitch"
                         :labels="{checked: 'On', unchecked: 'Off'}"/>
        </div>
      </template>
      <ul class="list-unstyled robot-log-ul px-3 py-2" ref="robotLogUl">
        <li v-for="log in robotLogList" :key="log.timestamp">
          {{log.timestamp|formatLogTime}} {{log.level}} {{log.msg}}
        </li>
      </ul>
    </b-card>
  </div>
</template>

<script>
    import {updateRobot} from "../api";
    import moment from 'moment'

    export default {
        name: 'RobotLog',
        props: {
            robotEnabled: Boolean,
            robotStreamKey: String,
        },
        data() {
            return {
                robotSwitchDisabled: false,
                robotLogList: [],
                hideStreamKey: true,
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
                    if (data.topic === 'log') {
                        vm.robotLogList.push(data);
                        if (vm.robotLogList.length > 100) {
                            vm.robotLogList.shift()
                        }
                        vm.$nextTick(() => {
                            vm.$refs.robotLogUl.scrollTop = vm.$refs.robotLogUl.scrollHeight - vm.$refs.robotLogUl.clientHeight
                        })
                    }
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
        computed: {
            maskedRobotStreamKey() {
                return '*'.repeat(this.robotStreamKey.length)
            }
        },
        mounted() {
            // 组件创建完后获取数据，
            // 此时 data 已经被 observed 了
            this.subscribe()
        },
        filters: {
            formatLogTime: function (value) {
                return moment(value).format('HH:MM:DD')
            }
        }
    }
</script>

<style scoped>
  .robot-log-ul {
    max-height: 20rem;
    overflow-y: scroll;
  }

  .card-body {
    padding: 0;
  }
</style>
