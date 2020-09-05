<template>
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
        <param-preview
            :parameters="
              strategyParametersView && strategyParametersView.parameters
            "
        ></param-preview>
      </b-card>
      <b-modal
          button-size="sm"
          size="md"
          id="param-form-modal"
          centered
          title="参数设置"
      >
        <param-form
            ref="paramForm"
            :fields="
              strategyParametersView && strategyParametersView.parameters
            "
        ></param-form>
        <template v-slot:modal-footer="{ ok }">
          <b-button size="sm" variant="primary" @click="onSubmit(ok, $event)"
          >确认
          </b-button
          >
        </template>
      </b-modal>
    </b-col>
  </b-row>
</template>

<script>
import LogPanel from "./RobotLogView";
import ParamPreview from "../components/ParamPreview";
import ParamForm from "../components/ParamForm";
import {getRobotsId, postRobotsIdStrategyParameters} from "../api";
import formatterMixin from "@/mixins/formatter"

export default {
  name: "robot-view",
  data() {
    return {
      logList: [],
      robotId: null,
      strategyParametersView: null,
    };
  },
  mixins: [formatterMixin],
  components: {
    LogPanel,
    ParamPreview,
    ParamForm,
  },
  methods: {
    async onSubmit(ok, event) {
      event.preventDefault();
      let data = {
        "type": "robots",
        "strategy_parameters": JSON.stringify(this.$refs.paramForm.form)
      }
      try {
        await postRobotsIdStrategyParameters(
            this.$route.params.id,
            this.formatter.serialize(data)
        );
        await this.getRobot();
        this.$bvModal.hide("param-form-modal");
      } catch (error) {
        if (error.response) {
          if (error.response.status === 500) {
            this.$bvToast.toast(`服务端错误: ${error.response.status}`, {
              title: "更新失败",
              autoHideDelay: 3000,
              toaster: "b-toaster-top-center",
              variant: "danger",
              appendToast: false,
            });
          } else if (error.response.status === 400) {
            // this.paramFormErrors = error.response.data.errors;
            // todo
          } else {
            this.$bvToast.toast(error.message, {
              title: "数据获取失败",
              autoHideDelay: 3000,
              toaster: "b-toaster-top-center",
              variant: "danger",
              appendToast: false,
            });
          }
        } else {
          this.$bvToast.toast(error.message, {
            title: "数据获取失败",
            autoHideDelay: 3000,
            toaster: "b-toaster-top-center",
            variant: "danger",
            appendToast: false,
          });
        }
      }
    },
    async getRobot() {
      try {
        const robotRes = await getRobotsId(this.$route.params.id);
        const result = this.formatter.deserialize(robotRes.data)
        this.robotId = result.id;
        this.strategyParametersView = result["strategy_parameters_view"];
      } catch (error) {
        if (error.response) {
          this.$bvToast.toast('机器人数据获取失败', {
            title: '机器人数据获取失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '机器人数据获取失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        }
      }
    },
  },
  async mounted() {
    await this.getRobot();
  },
};
</script>

<style scoped></style>
