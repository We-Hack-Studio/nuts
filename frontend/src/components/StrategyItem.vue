<template>
  <b-card>
    <div>
      <b-media no-body>
        <b-media-aside vertical-align="center">
          <b-icon-graph-up font-scale="1.5" class="text-muted"></b-icon-graph-up>
        </b-media-aside>
        <b-media-body class="ml-3">
          <h5><a href="">{{strategyTemplate.name}}</a></h5>
          <div class="small text-muted">{{strategyTemplate.description}}</div>
        </b-media-body>
      </b-media>
    </div>
  </b-card>
</template>

<script>
    export default {
        name: 'StrategyTemplateItem',
        props: {
            strategyTemplate: Object,
        },
    }
</script>

<style scoped>
</style>
