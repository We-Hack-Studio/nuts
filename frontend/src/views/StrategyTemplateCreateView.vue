<template>
  <b-row>
    <b-col md="6">
      <strategy-template-create-form></strategy-template-create-form>
    </b-col>
  </b-row>
</template>

<script>
    import StrategyTemplateCreateForm from "../components/StrategyTemplateCreateForm";

    export default {
        name: "strategy-template-create",
        components: {
            StrategyTemplateCreateForm
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