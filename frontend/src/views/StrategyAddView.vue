<template>
  <div class="mx-sm-2 mx-md-3">
    <b-row>
      <b-col md="8">
        <b-card
            header="新增策略"
            header-tag="header"
        >
          <strategy-form></strategy-form>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import StrategyForm from "../components/StrategyForm";

export default {
  name: "StrategyAddView",
  components: {
    StrategyForm
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