<template>
  <b-row>
    <b-col md="6">
      <robot-form></robot-form>
    </b-col>
  </b-row>
</template>

<script>
    import RobotForm from "../components/RobotCreateForm";

    export default {
        data() {
            return {}
        },
        components: {
            RobotForm,
        },
    }
</script>

<style scoped>

</style>
