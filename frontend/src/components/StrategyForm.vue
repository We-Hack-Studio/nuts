<template>
  <b-form @submit="onSubmit">
    <b-form-group
        label="名称："
        label-for="id_name"
    >
      <b-form-input
          id="id_name"
          v-model="form.name"
          type="text"
          required
          :state="formErrors.name===undefined?null:false"
      ></b-form-input>
      <b-form-invalid-feedback :state="formErrors.name===undefined?null:false">
        {{ formErrors.name !== undefined && formErrors.name[0] }}
      </b-form-invalid-feedback>
    </b-form-group>
    <b-form-group
        label="简介："
        label-for="id_brief"
    >
      <b-form-input
          id="id_brief"
          v-model="form.brief"
          type="text"
          :state="formErrors.brief===undefined?null:false"
      ></b-form-input>
      <b-form-invalid-feedback :state="formErrors.brief===undefined?null:false">
        {{ formErrors.brief !== undefined && formErrors.brief[0] }}
      </b-form-invalid-feedback>
    </b-form-group>
    <b-form-group
        label="详细描述："
        label-for="id_description"
    >
      <b-form-textarea
          id="id_description"
          v-model="form.description"
          rows="3"
          max-rows="6"
          :state="formErrors.description===undefined?null:false"
      ></b-form-textarea>
      <b-form-invalid-feedback :state="formErrors.description===undefined?null:false">
        {{ formErrors.description !== undefined && formErrors.description[0] }}
      </b-form-invalid-feedback>
    </b-form-group>
    <b-form-group
        label="规范："
        label-for="id_specification"
    >
      <b-tabs content-class="mt-3" small>
        <b-tab title="文本模式" active @click="specInputMode='text'">
          <b-form-textarea
              id="textarea"
              v-model="form.specificationText"
              placeholder=""
              rows="3"
              max-rows="6"
              :state="formErrors.specification===undefined?null:false"
          ></b-form-textarea>
          <b-form-invalid-feedback :state="formErrors.specification===undefined?null:false">
            {{ formErrors.specification !== undefined && formErrors.specification[0] }}
          </b-form-invalid-feedback>
        </b-tab>
        <b-tab title="编辑模式" @click="specInputMode='ui'">
          <JsonEditor
              :options="{
                            confirmText: '确认',
                            cancelText: '取消',
                        }"
              :objData="form.specificationUI"
              v-model="form.specificationUI">
          </JsonEditor>
        </b-tab>
      </b-tabs>
    </b-form-group>
    <b-button type="submit" variant="primary" class="mt-2">提交</b-button>
  </b-form>
</template>

<script>
import {createStrategy} from "@/api/strategy";

export default {
  name: 'StrategyForm',
  data() {
    return {
      specInputMode: "text",
      form: {
        name: '',
        brief: '',
        description: '',
        specificationUI: {},
        specificationText: "",
      },
      submitting: false,
      formErrors: {},
    }
  },
  methods: {
    async onSubmit(e) {
      e.preventDefault()
      this.submitting = true
      let data = {
        "name": this.form.name,
        "brief": this.form.brief,
        "description": this.form.description,
        "specification": this.specInputMode === "ui" ? JSON.stringify(this.form.specificationUI) : this.form.specificationText,
      }
      try {
        await createStrategy(data)
        await this.$router.push({name: 'strategy-list'})
        this.submitting = false
      } catch (error) {
        if (error.response) {
          if (error.response.status === 500) {
            this.$bvToast.toast('服务端错误', {
              title: '新增策略失败',
              autoHideDelay: 2000,
              toaster: 'b-toaster-top-right',
              variant: 'danger',
              appendToast: false
            });
          } else if (error.response.status === 400) {
            // form validation error
            this.formErrors = error.response.data
          }
        } else {
          this.$bvToast.toast(error.message, {
            title: '新增策略失败',
            autoHideDelay: 2000,
            toaster: 'b-toaster-top-right',
            variant: 'danger',
            appendToast: false
          });
        }
      }
    },
  }
}
</script>
<style scoped>
</style>
