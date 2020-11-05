<template>
  <b-card no-body header-tag="header" bg-variant="dark" text-variant="white">
    <template v-slot:header>
      <div>
        <span>日志监控</span>
      </div>
    </template>
    <ul class="list-unstyled robot-log-ul px-3 pt-2 pb-5 small mb-0 log-content" ref="robotLogUl">
      <li v-for="(log, index) in logList" :key="index">
        <span v-if="log.timestamp">{{ log.timestamp | timeFormatter }}</span>
        <span v-if="log.level" :class="['mx-1', levelColor(log.level)]">{{ log.level.toUpperCase() }}</span>
        {{ log.text }}
      </li>
      <li v-if="!logList.length">正在等待接收日志......</li>
    </ul>
  </b-card>
</template>

<script>
import {mapState} from "vuex";
import moment from "moment";

export default {
  name: "LogPanel",
  data() {
    return {
      logList: [],
      robotId: null,
      ws: null,
    };
  },
  watch: {
    logList() {
      this.updateScroll();
    },
  },
  filters: {
    timeFormatter(timestamp) {
      return moment(timestamp).format('YYYY-MM-DD HH:mm:ss');
    },
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
    updateScroll() {
      this.$nextTick(() => {
        this.$refs.robotLogUl.scrollTop =
            this.$refs.robotLogUl.scrollHeight - this.$refs.robotLogUl.clientHeight;
      });
    },
    levelColor(level) {
      switch (level.toUpperCase()) {
        case 'DEBUG':
          return 'text-secondary';
        case 'INFO':
          return 'text-info';
        case 'WARNING':
          return 'text-warning';
        case 'ERROR':
          return 'text-danger';
        case 'SUCCESS':
          return 'text-success';
        default:
          return '';
      }
    },
  },
};
</script>

<style>
.log-content {
  height: 360px;
  /* max-height: 70vh; */
  padding-bottom: 50px;
  overflow-y: scroll;
}

.log-content::-webkit-scrollbar-track {
  background-color: #343a40;
  border-radius: 8px;
}

.log-content::-webkit-scrollbar-thumb {
  background-color: black;
  border-radius: 5px;
}

.log-content::-webkit-scrollbar {
  width: 6px;
}
</style>
