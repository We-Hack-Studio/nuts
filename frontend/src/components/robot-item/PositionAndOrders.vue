<template>
    <div>
        <b-card no-body>
            <b-tabs card>
                <b-tab title="仓位" active>
                    <b-card-text v-if="positionStore">
                        <div
                            :key="index"
                            v-for="(position, index) in positionStore.positions"
                            class="d-flex justify-content-between"
                        >
                            <div>
                                <div class="small text-secondary">持仓数量</div>
                                <div :class="getProfitColorClass(position)">{{ position.qty * position.side }}</div>
                            </div>
                            <div>
                                <div class="small text-secondary">均价 / 爆仓点位</div>
                                <div>{{ position.avgPrice }} / {{ position.liqPrice }}</div>
                            </div>
                            <div>
                                <div class="small text-secondary">未实现盈亏</div>
                                <div :class="getUplColor(position)">{{ position.unrealizedPnl }}</div>
                            </div>
                        </div>
                    </b-card-text>
                </b-tab>
                <b-tab title="订单"><b-card-text>Tab contents 2</b-card-text></b-tab>
            </b-tabs>
        </b-card>
    </div>
</template>

<script>
export default {
    props: ['positionStore'],
    methods: {
        getProfitColorClass(position) {
            return position.side > 0 ? 'text-success' : 'text-danger';
        },
        getUplColor(position) {
            return position.unrealizedPnl > 0 ? 'text-success' : 'text-danger';
        },
    },
    mounted() {
        console.log(this.positionStore);
    },
};
</script>

<style></style>
