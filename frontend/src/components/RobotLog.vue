<template>
  <div>
    <b-card header-tag="header" footer-tag="footer">
      <template v-slot:header>
        <h6 class="mb-0">日志监控</h6>
      </template>
      <p v-for="log in robotLogList" :key="log.datetime">{{log.datetime}} {{log.msg}}</p>
    </b-card>
  </div>
</template>

<script>
    export default {
        name: 'RobotLog',
        data() {
            return {
                robotLogList: []
            }
        },
        methods: {
            subscribe() {
                let vm = this
                let robotSocket = new WebSocket(
                    'ws://127.0.0.1:7000/ws/streams/'
                );

                robotSocket.onmessage = function (e) {
                    let data = JSON.parse(e.data);
                    vm.robotLogList.push({
                        datetime: data.datetime,
                        msg: data.data.msg,
                    });
                };

                robotSocket.onclose = function () {
                    console.error('Robot socket closed unexpectedly');
                };

                robotSocket.onopen = function () {
                    console.info("Websocket opened!");
                    let message = JSON.stringify({
                        'cmd': "sub",
                        'params': ['robot.' + vm.$route.params.id],
                        "id": "fisher"
                    })
                    robotSocket.send(message);
                };
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
