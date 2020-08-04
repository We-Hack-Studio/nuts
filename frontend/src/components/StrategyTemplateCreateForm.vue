<template>
  <b-form @submit="onSubmit">
    <b-form-group
        id="input-group-1"
        label="策略代码："
        label-for="input-1"
    >
      <b-form-input
          id="input-1"
          v-model="form.code"
          type="text"
          required
      ></b-form-input>
    </b-form-group>

    <b-form-group
        id="input-group-2"
        label="策略名称："
        label-for="input-1"
    >
      <b-form-input
          id="input-1"
          v-model="form.name"
          type="text"
          required
      ></b-form-input>
    </b-form-group>
    <div>
    </div>
    <b-form-group
        label="策略参数规格："
        label-for="input-1"
    >
      <b-tabs content-class="mt-3" small>
        <b-tab title="编辑模式" active @click="paramSpecMode='ui'">
          <JsonEditor
              :options="{
            confirmText: '确认',
            cancelText: '取消',
        }"
              :objData="form.paramSpecUI"
              v-model="form.paramSpecUI">
          </JsonEditor>
        </b-tab>
        <b-tab title="文本模式" @click="paramSpecMode='text'">
          <b-form-textarea
              id="textarea"
              v-model="form.paramSpecText"
              placeholder=""
              rows="3"
              max-rows="6"
          ></b-form-textarea>
        </b-tab>
      </b-tabs>
    </b-form-group>
    <b-button type="submit" variant="primary" class="mt-2">提交</b-button>
  </b-form>
</template>

<script>
import {createStrategyTemplate} from "@/api";

export default {
  name: 'StrategyTemplateCreateForm',
  data() {
    return {
      paramSpecMode: "ui",
      form: {
        code: '',
        name: '',
        paramSpecUI: null,
        paramSpecText: null,
      },
    }
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      let data = {
        "code": this.form.code,
        "name": this.form.name,
        "param_spec": this.paramSpecMode === "ui" ? this.form.paramSpecUI : this.form.paramSpecText,
      }
      createStrategyTemplate(data).then(() => {
        this.$router.push('/strategy-template/list')
      }).catch(err => {
        console.log(err.data);
      })
    },
  }
}
</script>
<style scoped>
</style>
