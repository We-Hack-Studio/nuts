<template>
  <b-card class="mt-2">
    <b-form @submit="onSubmit">
      <b-form-row>
        <b-col md="3">
          <label>名字:</label>
        </b-col>
        <b-col md="9">
          <b-form-input type="text" v-model="form.name"></b-form-input>
        </b-col>
      </b-form-row>
      <b-form-row class="mt-2">
        <b-col md="3">
          <label>策略:</label>
        </b-col>
        <b-col md="9">
          <b-form-select
              id="idStrategyTemplate"
              v-model="form.strategyTemplate"
              :options="strategyTemplateOptions"

              required
          ></b-form-select>
        </b-col>
      </b-form-row>
      <b-form-row class="mt-2">
        <b-col md="3">
          <label>启用:</label>
        </b-col>
        <b-col md="9">
          <b-form-checkbox
              id="id_enable"
              v-model="form.enable"
              name="enable"
              value=true

              unchecked-value=false
          >
          </b-form-checkbox>
        </b-col>
      </b-form-row>
      <b-button block type="submit" variant="primary" class="mt-3">更新</b-button>
    </b-form>
  </b-card>
</template>

<script>
import {getRobotsId, patchRobotsId, getStrategies} from "../api";

export default {
  name: 'RobotUpdateForm',
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
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      let data = {
        "name": this.form.name,
        "enable": this.form.enable,
        "strategy_template": this.form.strategyTemplate,
      }
      patchRobotsId(data).then(() => {
        this.$router.push(`/robot/${this.robotId}`)
      }).catch(err => {
        console.log(err.data);
      })
    },
    setStrategyTemplateOptions(data) {
      this.strategyTemplateOptions = data.map(st => ({value: st.id, text: st.name}))
    },
    initRobotForm(data) {
      this.form = {
        name: data.name,
        enabled: data.enabled,
        strategy: data['strategy_template'],
      }
    },
  },
  mounted() {
    getStrategies().then(response => {
      this.setStrategyTemplateOptions(response.data)
    }).catch(err => {
      this.$bvToast.toast(`无法获取策略，错误信息：${err.data || '未知错误'}`, {
        title: '数据获取失败',
        autoHideDelay: 3000,
        toaster: 'b-toaster-top-right',
        variant: 'danger',
        appendToast: false
      });
    });

    getRobotsId(this.$route.params.id).then(response => {
      this.initRobotForm(response.data)
    }).catch(err => {
      this.$bvToast.toast(`无法获取机器人数据，错误信息：${err.data || '未知错误'}`, {
        title: '数据获取失败',
        autoHideDelay: 3000,
        toaster: 'b-toaster-top-right',
        variant: 'danger',
        appendToast: false
      });
    });
  },
}
</script>