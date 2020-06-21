<template>
  <b-row>
    <b-col md="4">
      <robot-log></robot-log>
    </b-col>
    <b-col md="8">
      <grid-table></grid-table>
    </b-col>
  </b-row>
</template>

<script>
    import RobotLog from "../components/RobotLog";
    import GridTable from "../components/GridTable";

    export default {
        name: "Ranking",
        components: {
            RobotLog,
            GridTable,
        },
    }
</script>

<style scoped>

</style>