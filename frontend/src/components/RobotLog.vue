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
            robotLogList: Array,
        },
        data() {
            return {
                robotSwitchDisabled: false,
                hideStreamKey: true,
            }
        },
        methods: {
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
        watch: {
            robotLogList() {
                this.$nextTick(() => {
                    this.$refs.robotLogUl.scrollTop = this.$refs.robotLogUl.scrollHeight - this.$refs.robotLogUl.clientHeight
                })
            }
        },
        filters: {
            formatLogTime: function (value) {
                return moment(value).format('YYYY-MM-DD HH:mm:ss')
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
