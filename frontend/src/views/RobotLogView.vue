<template>
  <div>
    <LogPanel :logList="logList"></LogPanel>
  </div>
</template>

<script>
import LogPanel from "@/components/LogPanel";
import { mapState } from "vuex";

export default {
  data() {
    return {
      logList: [],
    };
  },
  computed: {
    robotId() {
      return this.$route.params.id;
    },
    ...mapState(["authToken"]),
  },
  mounted() {
    // 建立 websocket 连接
    this.initWebsocket();
  },
  methods: {
    initWebsocket() {
      // 初始化weosocket
      const wsuri = `${window.conf.websocketApiUri}`; // 这个地址由后端童鞋提供
      this.websock = new WebSocket(wsuri);
      this.websock.onmessage = (message) => {
        message = JSON.parse(message.data);
        if (message.code) {
          if (message.code === 200) {
            this._sendInfo({
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
              text: "认证失败, 订阅中...",
            });
          }
        } else if (message.category === "robotLog") {
          this.logList.push(message.data);
        } else {
          console.log(message);
        }
      };
      this.websock.onopen = () => {
        console.log("on open");
        this.logList.push({
          timestamp: Date.now(),
          level: "info",
          text: "已建立 websocket 连接, token 认证中...",
        });
        this._sendInfo({
          cmd: "auth",
          token: this.authToken,
        });
      };
      this.websock.onerror = (event) => {
        console.log("error");
        console.log("error event:", event);
      };
      this.websock.onclose = (event) => {
        console.log("close event", event);
        this.logList.push({
          timestamp: Date.now(),
          level: "error",
          text: "Websocket 连接已断开！",
        });
        this.reConnect();
      };

      // setInterval(this.checkConnection, 5000);
    },
    reConnect() {
      setTimeout(() => {
        this.logList.push({
          timestamp: Date.now(),
          level: "info",
          text: "正在尝试重新建立 WebSocket 连接",
        });
        this.initWebsocket();
      }, 5000);
    },
    // checkConnection() {
    //   this._sendInfo({
    //     cmd: "auth",
    //     token: this.authToken,
    //   });
    // },

    _sendInfo(info) {
      this.websock.send(JSON.stringify(info));
    },
  },
  components: {
    LogPanel,
  },
};
</script>

<style></style>
