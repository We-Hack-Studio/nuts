<template>
    <div class="justify-content-between d-flex">
        <div>
            <div class="small text-secondary">类型</div>
            <div>限价委托</div>
        </div>
        <div>
            <div class="small text-secondary">方向</div>
            <div>卖</div>
        </div>
        <div>
            <div class="small text-secondary">价格</div>
            <div>{{ order.price }}</div>
        </div>
        <div>
            <div class="small text-secondary">数量</div>
            <div :class="getProfitColorClass(order)">{{ order.qty }}</div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PositionItem',
    props: {
        order: Object,
    },
    methods: {
        getProfitColorClass(order) {
            return order.side > 0 ? 'text-success' : 'text-danger';
        },
    },
};
</script>
<style scoped></style>
