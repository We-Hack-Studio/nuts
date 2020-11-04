<template>
    <div>
        <b-card no-body class="mt-3" header-tag="header" bg-variant="dark" text-variant="white">
            <template v-slot:header>
                <div class="d-flex justify-content-between">
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
    </div>
</template>

<script>
import moment from 'moment';

export default {
    name: 'LogPanel',
    props: ['logList'],
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
    methods: {
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
