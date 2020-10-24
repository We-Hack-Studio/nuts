<template>
  <div v-if="parameters">
    <div
        v-for="paramItem in parameters"
        :key="paramItem.code"
        class="d-flex align-items-center mb-2"
    >
      <div class="label">
        <span
            v-b-tooltip.hover
            :class="['mr-2', underLineClass(paramItem)]"
            :title="paramItem.description"
        >{{ paramItem.name }}</span>
      </div>
      <span>{{ formatValue(paramItem) || '-' }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: "ParamPreview",
  props: ["parameters"],
  methods: {
    underLineClass(item) {
      if (item.description) {
        return "underline";
      }
      return "";
    },
    formatValue(item) {
      if (item.type === "enum") {
        const itemArray = item.items.find((ele) => ele.value === item.value);
        if (itemArray) {
          return itemArray.display;
        }
        return "";
      }
      return item.value;
    },
  },
};
</script>

<style scoped>
.label {
  display: block;
  min-width: 120px;
}

.underline {
  border-bottom: 1px dotted #888;
}
</style>