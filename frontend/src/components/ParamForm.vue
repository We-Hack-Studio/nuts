<template>
  <b-form>
    <b-form-group
      v-for="field in fields"
      :key="field.code"
      :label="field.name"
      :description="field.description"
    >
      <component
        v-model="form[field.code]"
        v-bind:is="fieldFactory(field.type)"
        :items="field.items"
      ></component>
    </b-form-group>
  </b-form>
</template>

<script>
import { BFormInput } from "bootstrap-vue";
import SelectItem from "./ParamFormSelectItem";

export default {
  name: "ParamPreview",
  props: {
    fields: Array,
  },
  mounted() {
    console.log(this.fields);
    this.initForm();
  },
  data() {
    return {
      form: {},
      strategyTemplateOptions: [],
    };
  },
  components: { BFormInput },

  methods: {
    initForm() {
      this.fields.forEach((item) => {
        this.$set(this.form, item.code, item.value);
        // this.$set(this.form, item.code, 1);
      });
    },
    fieldFactory: function (fieldType) {
      switch (fieldType) {
        case "integer":
        case "float":
          return BFormInput;
        case "enum":
          return SelectItem;
        default:
          return BFormInput;
      }
    },
  },
};
</script>

<style scoped>
fieldset {
  margin-bottom: 1rem;
  padding: 0;
  border: 0;
}
</style>