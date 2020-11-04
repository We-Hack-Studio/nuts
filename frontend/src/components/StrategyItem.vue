<template>
  <b-card>
    <div>
      <b-media no-body>
        <b-media-aside vertical-align="center">
          <b-icon-graph-up font-scale="1.5" class="text-muted"></b-icon-graph-up>
        </b-media-aside>
        <b-media-body class="ml-3">
          <h5>
            <router-link :to="{ name: 'strategy-detail', params: { id: strategy.id } }">
              {{ strategy.name }}
            </router-link>
          </h5>
          <div class="small text-muted">{{ strategy.brief }}</div>
        </b-media-body>
      </b-media>
    </div>
  </b-card>
</template>

<script>
export default {
  name: 'StrategyItem',
  props: {
    strategy: Object,
  },
}
</script>

<style scoped>
</style>
