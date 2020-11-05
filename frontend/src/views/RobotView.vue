<template>
  <b-row class="m-1">
    <b-col md="8">
      <log-panel/>
      <b-card no-body class="mt-3">
        <b-tabs card>
          <b-tab title="持有仓位" active>
            <position :position-store="positionStore"></position>
          </b-tab>
          <b-tab title="当前委托">
            <order :order-store="orderStore"></order>
          </b-tab>
        </b-tabs>
      </b-card>
      <!--      <asset-chart/>-->
    </b-col>
    <b-col md="4">
      <overview :overview-data="overviewData"/>
      <b-card header-tag="header" class="mt-3">
        <template v-slot:header>
          <div class="d-flex justify-content-between align-items-center">
            <span class="h6">参数预览</span>
            <a href="#" v-b-modal.param-form-modal>
              <b-icon-pencil-square></b-icon-pencil-square>
            </a>
          </div>
        </template>
        <param-preview :parameters="strategySpecView && strategySpecView.parameters"></param-preview>
      </b-card>
    </b-col>
    <b-modal button-size="sm" size="md" id="param-form-modal" scrollable centered title="参数设置">
      <param-form ref="paramForm" :fields="strategySpecView && strategySpecView.parameters"></param-form>
      <template v-slot:modal-footer="{ ok }">
        <b-button size="sm" variant="primary" @click="onSubmit(ok, $event)">确认</b-button>
      </template>
    </b-modal>
  </b-row>
</template>

<script>
import LogPanel from '@/components/robot-console/LogPanel';
import ParamPreview from '../components/ParamPreview';
import ParamForm from '../components/ParamForm';
import Position from '../components/robot-console/Position';
// import AssetChart from '../components/robot-console/AssetChart';
import Overview from '../components/robot-console/Overview';
import Order from "@/components/robot-console/Order";
import {getRobotsId} from '@/api';
import {getRobotsIdStrategySpecView, patchRobotsIdStrategyParameters} from '@/api/robot';

export default {
  name: 'RobotView',
  data() {
    return {
      logList: [],
      robotId: null,
      strategySpecView: null,
      overviewData: null,
      positionStore: null,
      orderStore: null,
    };
  },
  components: {
    LogPanel,
    ParamPreview,
    ParamForm,
    Overview,
    Position,
    Order,
    // AssetChart,
  },
  methods: {
    async onSubmit(ok, event) {
      event.preventDefault();
      let data = this.$refs.paramForm.form;
      try {
        await patchRobotsIdStrategyParameters(this.$route.params.id, data);
        await this.getRobot();
        this.$bvModal.hide('param-form-modal');
      } catch (error) {
        if (error.response) {
          if (error.response.status === 500) {
            this.$bvToast.toast(`服务端错误: ${error.response.status}`, {
              title: '更新失败',
              autoHideDelay: 3000,
              toaster: 'b-toaster-top-center',
              variant: 'danger',
              appendToast: false,
            });
          } else if (error.response.status === 400) {
            // this.paramFormErrors = error.response.data.errors;
            // todo
          } else {
            this.$bvToast.toast(error.message, {
              title: '数据获取失败',
              autoHideDelay: 3000,
              toaster: 'b-toaster-top-center',
              variant: 'danger',
              appendToast: false,
            });
          }
        } else {
          this.$bvToast.toast(error.message, {
            title: '数据获取失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false,
          });
        }
      }
    },
    async getRobot() {
      try {
        const robotRes = await getRobotsId(this.$route.params.id);
        const result = robotRes.data;
        this.robotId = result.id;
        this.positionStore = result['position_store'];
        this.orderStore = result['order_store'];
        this.overviewData = {
          name: result.name,
          pair: result.pair,
          marketType: result['market_type'],
          RobotId: this.robotId,
          strategyName: result['strategy_name'],
          targetCurrency: result['target_currency'],
          baseCurrency: result['base_currency'],
          quoteCurrency: result['quote_currency'],
          durationDisplay: result['duration_display'],
          marketTypeDisplay: result['market_type_display'],
          exchangeName: result.exchange.name,
          testNet: result['test_net'],
          enabled: result.enabled,
          totalPrincipal: result['asset_record']['total_principal'],
          totalBalance: result['asset_record']['total_balance'],
          totalPnlAbs: result['asset_record']['total_pnl_abs'],
          totalPnlAbs24h: result['asset_record']['total_pnl_abs_24h'],
          totalPnlRelPtg: result['asset_record']['total_pnl_rel_ptg'],
          totalPnlRelPtg24h: result['asset_record']['total_pnl_rel_ptg_24h'],
        };
      } catch (error) {
        if (error.response) {
          this.$bvToast.toast('获取机器人数据失败', {
            title: '获取机器人数据失败',
            autoHideDelay: 2000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false,
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '获取机器人数据失败',
            autoHideDelay: 2000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false,
          });
        }
      }
    },
    async getStrategySpecView() {
      try {
        const response = await getRobotsIdStrategySpecView(this.$route.params.id);
        this.strategySpecView = response.data;
      } catch (error) {
        if (error.response) {
          this.$bvToast.toast('策略视图获取失败', {
            title: '策略视图获取失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false,
          });
        } else {
          this.$bvToast.toast(error.message, {
            title: '策略视图获取失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false,
          });
        }
      }
    },
  },
  async mounted() {
    await this.getRobot();
    await this.getStrategySpecView();
  },
};
</script>

<style scoped></style>
