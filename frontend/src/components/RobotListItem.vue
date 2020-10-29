<template>
    <b-card class="mb-4 card">
        <div class="d-flex align-items-center">
            <span :class="['mr-1', 'd-inline-flex', robotStatusClass]">
                <b-icon icon="circle-fill" font-scale="0.6" :animation="robotStatusAnimation"></b-icon>
            </span>
            <router-link :to="{ name: 'robot', params: { id: robot.robotId } }" class="font-weight-bold text-body">
                <span class="mr-2">{{ robot.name }}</span>
                <span class="text-muted font-weight-light">{{ robot.exchangeNameZh }} {{ robot.pair }}</span>
            </router-link>
            <span class="ml-auto action-buttons">
                <router-link :to="{ name: 'robot-update', params: { id: robot.robotId } }" class="mr-2">
                    <b-icon-pencil-square></b-icon-pencil-square>
                </router-link>
                <a href="#" class="text-danger" @click="showMsgBox">
                    <b-icon-trash></b-icon-trash>
                </a>
            </span>
        </div>
        <div class="d-flex justify-content-between mt-2">
            <span>
                <span class="small text-muted">收益率</span><br />
                <span :class="[profitColorClass, 'h6']">{{ robot.profitRatioPtg }}</span></span
            >
            <span>
                <span class="small text-muted">收益额({{ robot.targetCurrency }})</span><br />
                <span :class="profitColorClass">
                    <small>{{ robot.profit | roundByCurrency(robot.targetCurrency) }}</small>
                </span></span
            >
            <span>
                <span class="small text-muted">本金({{ robot.targetCurrency }})</span><br />
                <span class="">
                    <small> {{ robot.principal | roundByCurrency(robot.targetCurrency) }}</small>
                </span>
            </span>
            <span>
                <span class="small text-muted">余额({{ robot.targetCurrency }})</span><br /><span class="">
                    <small>{{ robot.balance | roundByCurrency(robot.targetCurrency) }}</small>
                </span>
            </span>
        </div>
        <!-- <div class="text-muted mt-2">
            <span class="mr-2">{{ robot.exchangeNameZh }}</span>
            <span>{{ robot.pair }}</span>
            <span class="float-right">{{ robot.durationDisplay }}</span>
        </div> -->
        <hr />
        <div class="small d-flex justify-content-between">
            <div class="d-inline-block">
                <span class="mr-1 text-muted">较前日</span>
                <span :class="[profit24hColorClass, 'mr-1']">
                    <b-icon-caret-up-fill v-if="robot.profit24h > 0"></b-icon-caret-up-fill>
                    <b-icon-caret-down-fill v-if="robot.profit24h < 0"></b-icon-caret-down-fill>
                    {{ robot.profitRatioPtg24h }}
                </span>
                <span :class="profit24hColorClass">
                    {{ robot.profit24h | roundByCurrency(robot.targetCurrency) }}
                    <span class="font-weight-light"> {{ robot.targetCurrency }}</span>
                </span>
            </div>
            <div class="d-inline-block">
                <b-icon icon="graph-up" class="mr-1"></b-icon>
                <span class=""> {{ robot.strategyName }} </span>
                <span class="text-muted"> {{ robot.durationDisplay }} </span>
            </div>
        </div>
    </b-card>
</template>

<script>
import moment from 'moment';
import { deleteRobotsId } from '../api';

export default {
    name: 'RobotListItem',
    props: {
        robot: Object,
    },
    computed: {
        robotStatusClass() {
            return moment().diff(this.robot.pingTime, 'seconds') < 60 ? 'text-success' : 'text-danger';
        },
        robotStatusAnimation() {
            return this.robotStatusClass === 'text-danger' ? '' : 'throb';
        },
        profitColorClass() {
            return this.robot.profit > 0 ? 'text-success' : this.robot.profit < 0 ? 'text-danger' : '';
        },
        profit24hColorClass() {
            return this.robot.profit24h > 0 ? 'text-success' : this.robot.profit24h < 0 ? 'text-danger' : '';
        },
    },
    filters: {
        roundByCurrency(value, currency) {
            switch (currency) {
                case 'BTC':
                    return value.toFixed(4);
                case 'USDT':
                    return value.toFixed(2);
                default:
                    return value;
            }
        },
    },
    methods: {
        async showMsgBox() {
            const confirm = await this.$bvModal.msgBoxConfirm('删除机器人将同时删除其所有资产统计数据。', {
                title: '确认删除？',
                size: 'sm',
                buttonSize: 'sm',
                okVariant: 'danger',
                okTitle: '确认',
                cancelTitle: '取消',
                footerClass: 'p-2',
                hideHeaderClose: false,
                centered: true,
            });
            if (!confirm) {
                return;
            }
            try {
                await deleteRobotsId(this.robot.robotId);
                this.$emit('refresh');
            } catch (error) {
                this.$bvToast.toast(`无法删除机器人数据，错误信息：${error.data || '未知错误'}`, {
                    title: '删除失败',
                    autoHideDelay: 3000,
                    toaster: 'b-toaster-top-right',
                    variant: 'danger',
                    appendToast: false,
                });
            }
        },
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
    margin: 40px 0 0;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    display: inline-block;
    margin: 0 10px;
}

a {
    color: #42b983;
}

.action-buttons {
    display: none;
}

.card:hover .action-buttons {
    display: inline-block;
}
</style>
