<template>
  <b-form-select :value="value" @input="$emit('select', $event)">
    <b-form-select-option
      v-for="item in options"
      :key="item.value"
      :value="item.value"
      :selected="item.value === value"
    >{{item.text}}</b-form-select-option>
  </b-form-select>
</template>

<script>
export default {
  props: ["items", "value"],
  computed: {
    options() {
      return this.items.map((item) => ({ value: item[0], text: item[1] }));
    },
  },
  model: {
    prop: "value",
    event: "select",
  },
};
</script>

<style>
</style>