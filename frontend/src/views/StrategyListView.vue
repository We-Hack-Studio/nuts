<template>
  <b-row>
    <b-col md="6">
      <strategy-item
          v-for="st in strategyTemplateList"
          :strategyTemplate="st"
          :key="st.id"
          class="mt-3">
      </strategy-item>
    </b-col>
  </b-row>
</template>

<script>
import StrategyItem from "../components/StrategyItem";
import {getStrategies} from "../api"

export default {
  name: "strategy-template-list",
  components: {
    StrategyItem
  },
  data() {
    return {
      strategyTemplateList: []
    }
  },
  methods: {
    setStrategyTemplateList(data) {
      this.strategyTemplateList = data.map(st => ({
        id: st.id,
        code: st.code,
        name: st.name,
        description: st.description,
      }))
    },
    loadStrategyTemplateList() {
      getStrategies().then(response => {
        this.setStrategyTemplateList(response.data.results)
      }).catch(err => {
        console.log(err.data);
      })
    }
  },
  mounted() {
    this.loadStrategyTemplateList()
  },
}
</script>

<style scoped>

</style>