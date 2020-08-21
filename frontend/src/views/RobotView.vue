<template>
  <b-container>
    <b-row>
      <b-col md="12">
        <log-panel :log-list="logList"></log-panel>
        <b-card header-tag="header" class="mt-3">
          <template v-slot:header>
            <div class="d-flex justify-content-between align-items-center">
              <span class="h6">参数预览</span>
              <a href="#" v-b-modal.param-form-modal>
                <b-icon-pencil-square></b-icon-pencil-square>
              </a>
            </div>
          </template>
          <param-preview></param-preview>
        </b-card>
        <b-modal button-size="sm" size="sm" id="param-form-modal" centered title="参数设置">
          <param-form :fields="formFields"></param-form>
          <template v-slot:modal-footer="{ok}">
            <b-button size="sm" variant="primary" @click="onSubmit(ok, $event)">
              确认
            </b-button>
          </template>
        </b-modal>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import LogPanel from "../components/LogPanel";
import ParamPreview from "../components/ParamPreview";
import ParamForm from "../components/ParamForm";
import {getRobot} from "../api";

export default {
  name: "Ranking",
  data() {
    return {
      logList: [],
      robotId: null,
      paramPreview: null,
    }
  },
  components: {
    LogPanel,
    ParamPreview,
    ParamForm,
  },
  computed: {
    formFields: function () {
      let fields = []
      if (this.paramPreview === null) {
        return fields
      }
      for (const key of Object.keys(this.paramPreview)) {
        fields.push(this.paramPreview[key])
      }
      return fields
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
    onSubmit(ok, evt) {
      evt.preventDefault()
    },
  },
  mounted() {
    getRobot(this.$route.params.id).then(response => {
      this.robotId = response.data.id
      this.paramPreview = response.data['param_preview']
      // this.subscribe()
    }).catch(err => {
      this.$bvToast.toast(`获取机器人数据失败，错误信息： ${err.data}`, {
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
