<template>
    <b-card class="mb-4 card">
        <div class="d-flex justify-content-between mt-2">
            <span>
                <span class="small text-muted">收益率</span><br />
                <span :class="[profitColorClass, 'h6']">{{ robot.profitRatioPtg }}</span></span
            >
            <span>
                <span class="small text-muted">收益额({{ robot.targetCurrency }})</span><br />
                <span :class="profitColorClass">
                    <small>{{ robot.profit | roundByCurrency(robot.targetCurrency) }}</small>
                </span>
            </span>
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
    </b-card>
</template>

<script>
export default {
    data() {
        return {
            robot: {
                balance: 100,
                principal: 80,
                profit: 20,
                profitRatioPtg: '25%',
            },
        };
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
