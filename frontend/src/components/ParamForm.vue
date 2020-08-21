<template>
  <b-form>
    <b-form-row v-for="field in fields" :key="field.code">
      <b-col md="3">
        <label>名字:</label>
      </b-col>
      <b-col md="9">
        <component v-bind:is="fieldFactory(field.type)"></component>
      </b-col>
    </b-form-row>
  </b-form>
</template>

<script>
import {BFormInput} from 'bootstrap-vue'

export default {
  name: "ParamPreview",
  props: {
    fields: Array,
  },
  data() {
    return {
      form: {
        name: '',
        enable: false,
        strategyTemplate: null,
      },
      strategyTemplateOptions: [],
    }
  },
  components: {BFormInput},

  methods: {
    fieldFactory: function (fieldType) {
      switch (fieldType) {
        case "integer":
        case "float":
          return BFormInput
        default:
          return BFormInput
      }
    }
  }
}
</script>

<style scoped>

</style>