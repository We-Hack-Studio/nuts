<template>
  <b-row>
    <b-col md="6">
      <strategy-template-item
          v-for="st in strategyTemplateList"
          :strategyTemplate="st"
          :key="st.id"
          class="mt-3">
      </strategy-template-item>
    </b-col>
  </b-row>
</template>

<script>
import StrategyTemplateItem from "../components/StrategyTemplateItem";
import {getStrategyTemplateList} from "../api"

export default {
  name: "strategy-template-list",
  components: {
    StrategyTemplateItem
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
      getStrategyTemplateList().then(response => {
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