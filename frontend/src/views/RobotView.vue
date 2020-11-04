<template>
    <b-row class="m-1">
        <b-col md="6">
            <position-card :robotDetail="robotDetail" />
            <position-and-orders :positionStore="positionStore" />
            <asset-line />
        </b-col>
        <b-col md="6">
            <robot-form />
        </b-col>
        <b-col md="12">
            <log-panel :log-list="logList"></log-panel>
        </b-col>
        <b-col>
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
                <b-button size="sm" variant="primary" @click="onSubmit(ok, $event)">确认 </b-button>
            </template>
        </b-modal>
    </b-row>
</template>

<script>
import LogPanel from './RobotLogView';
import ParamPreview from '../components/ParamPreview';
import ParamForm from '../components/ParamForm';
import PositionCard from '../components/robot-item/PositionCard';
import PositionAndOrders from '../components/robot-item/PositionAndOrders';
import AssetLine from '../components/robot-item/AssetLine';
import RobotForm from '../components/robot-item/RobotForm';
import { getRobotsId } from '@/api';
import { getRobotsIdStrategySpecView, patchRobotsIdStrategyParameters } from '@/api/robot';

export default {
    name: 'robot-view',
    data() {
        return {
            logList: [],
            robotId: null,
            strategySpecView: null,
            robotDetail: {},
            positionStore: null,
        };
    },
    components: {
        LogPanel,
        ParamPreview,
        ParamForm,
        PositionCard,
        PositionAndOrders,
        AssetLine,
        RobotForm,
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
                this.robotDetail = result;
                this.positionStore = result['position_store'];

                this.robotId = result.id;
            } catch (error) {
                if (error.response) {
                    this.$bvToast.toast('机器人数据获取失败', {
                        title: '机器人数据获取失败',
                        autoHideDelay: 3000,
                        toaster: 'b-toaster-top-center',
                        variant: 'danger',
                        appendToast: false,
                    });
                } else {
                    this.$bvToast.toast(error.message, {
                        title: '机器人数据获取失败',
                        autoHideDelay: 3000,
                        toaster: 'b-toaster-top-center',
                        variant: 'danger',
                        appendToast: false,
                    });
                }
            }
        },
        // async getRobotDetail() {
        //     const robotDetail = await this.getRobotDetail(this.$route.params.id);
        //     console.log(robotDetail);
        //     this.robotDetail = robotDetail.data;
        // },
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
