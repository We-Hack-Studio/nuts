<template>
  <b-row>
    <b-col md="6">
      <strategy-create-form></strategy-create-form>
    </b-col>
  </b-row>
</template>

<script>
import StrategyCreateForm from "../components/StrategyCreateForm";

export default {
  name: "strategy-template-create",
  components: {
    StrategyCreateForm
  },
  data() {
    return {}
  },
  methods: {},
  mounted() {
  },
}
</script>

<style scoped>

</style>