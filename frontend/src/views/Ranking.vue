<template>
  <b-list-group>
    <b-list-group-item href="#" class="flex-column align-items-start">
      <rank-item></rank-item>
    </b-list-group-item>
    <b-list-group-item href="#" class="flex-column align-items-start">
      <rank-item></rank-item>
    </b-list-group-item>
    <b-list-group-item href="#" class="flex-column align-items-start">
      <rank-item></rank-item>
    </b-list-group-item>
  </b-list-group>
</template>

<script>
    import RankItem from "../components/RankItem";

    export default {
        name: "Ranking",
        components: {
            RankItem
        },

    }
</script>

<style scoped>

</style>