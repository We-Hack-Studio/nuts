<template>
  <div>
    <LogPanel :logList="logList"></LogPanel>
  </div>
</template>

<script>
import LogPanel from "@/components/LogPanel";
import {mapState} from "vuex";

export default {
  data() {
    return {
      logList: [],
      robotId: null,
      ws: null,
    };
  },
  computed: {
    ...mapState(["authToken"]),
  },
  mounted() {
    this.robotId = this.$route.params.id;
    // 建立 websocket 连接
    this.initWebsocket();
  },
  beforeDestroy() {
    if (this.ws) {
      this._send({
        cmd: "unsub",
        topics: [`robot#${this.robotId}.log`],
      });
      const ws = this.ws;
      this.ws = null;
      ws.close();
    }
  },
  components: {
    LogPanel,
  },
  methods: {
    initWebsocket() {
      // 初始化weosocket
      const wsuri = `${window.conf.websocketApiUri}`; // 这个地址由后端童鞋提供
      this.ws = new WebSocket(wsuri);
      this.ws.onmessage = (message) => {
        message = JSON.parse(message.data);
        if (message.ping) {
          this._send({
            pong: message.ping,
          });
          return
        }

        if (message.code) {
          if (message.code === 200) {
            this._send({
              cmd: "sub",
              topics: [`robot#${this.robotId}.log`],
            });
            this.logList.push({
              timestamp: Date.now(),
              level: "success",
              text: "认证成功, 订阅中...",
            });
          } else if (message.code === 400) {
            this.logList.push({
              timestamp: Date.now(),
              level: "error",
              text: "认证失败",
            });
          }
        } else if (message.category === "robotLog") {
          this.logList.push(message.data);
        } else {
          console.log(message);
        }
      };
      this.ws.onopen = () => {
        this.logList.push({
          timestamp: Date.now(),
          level: "INFO",
          text: "已建立 websocket 连接, token 认证中...",
        });
        this._send({
          cmd: "auth",
          auth_token: this.authToken,
        });
      };
      this.ws.onerror = (event) => {
        console.log("error event:", event);
      };
      this.ws.onclose = () => {
        this.logList.push({
          timestamp: Date.now(),
          level: "ERROR",
          text: "Websocket 连接已断开！",
        });
        if (this.ws) {
          this.reconnect();
        }
      };

      // setInterval(this.checkConnection, 5000);
    },
    reconnect() {
      setTimeout(() => {
        this.logList.push({
          timestamp: Date.now(),
          level: "INFO",
          text: "正在尝试重新建立 WebSocket 连接...",
        });
        this.initWebsocket();
      }, 5000);
    },
    // checkConnection() {
    //   this._send({
    //     cmd: "auth",
    //     token: this.authToken,
    //   });
    // },

    _send(message) {
      this.ws.send(JSON.stringify(message));
    },
  },
};
</script>

<style></style>
