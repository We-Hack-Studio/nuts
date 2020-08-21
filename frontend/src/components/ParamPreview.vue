<template>
  <div>
    <div class="d-flex align-items-center">
      <span class="mr-1">最低价</span>
      <b-icon-info-circle class="mr-3" font-scale="0.5"></b-icon-info-circle>
      <span>12</span>
    </div>
    <div class="d-flex align-items-center">
      <span class="mr-1">最高价</span>
      <b-icon-info-circle class="mr-3" font-scale="0.5"></b-icon-info-circle>
      <span>12</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "ParamPreview",
  methods: {
    showParamForm: function () {
      this.$emit("showParamForm")
    }
  }
}
</script>

<style scoped>

</style>