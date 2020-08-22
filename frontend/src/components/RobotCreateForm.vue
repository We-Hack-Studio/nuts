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
          <label>交易所凭证:</label>
        </b-col>
        <b-col md="9">
          <b-form-select
              id="id_credential"
              v-model="form.credential"
              :options="credentialOptions"

              required
          ></b-form-select>
        </b-col>
      </b-form-row>
      <b-form-row class="mt-2">
        <b-col md="3">
          <label>交易对:</label>
        </b-col>
        <b-col md="9">
          <b-form-input type="text" v-model="form.pair"></b-form-input>
        </b-col>
      </b-form-row>
      <b-form-row class="mt-2">
        <b-col md="3">
          <label>市场类型:</label>
        </b-col>
        <b-col md="9">
          <b-form-select
              id="idMarketType"
              v-model="form.marketType"
              :options="marketTypeOptions"

              required
          ></b-form-select>
        </b-col>
      </b-form-row>

      <!-- spots -->
      <template v-if="form.marketType==='spots'">
        <b-form-row class="mt-2">
          <b-col md="3">
            <label>基础币种:</label>
          </b-col>
          <b-col md="9">
            <b-form-input type="text" v-model="form.baseCurrency"></b-form-input>
          </b-col>
        </b-form-row>
        <b-form-row class="mt-2">
          <b-col md="3">
            <label>计价币种:</label>
          </b-col>
          <b-col md="9">
            <b-form-input type="text" v-model="form.quoteCurrency"></b-form-input>
          </b-col>
        </b-form-row>
      </template>
      <b-form-row class="mt-2">
        <b-col md="3">
          <label>目标币种:</label>
        </b-col>
        <b-col md="9">
          <b-form-input type="text" v-model="form.targetCurrency"></b-form-input>
        </b-col>
      </b-form-row>
      <b-form-row class="mt-2">
        <b-col md="3">
          <label>策略模板:</label>
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
      <b-button block type="submit" variant="primary" class="mt-3">创建</b-button>
    </b-form>
  </b-card>
</template>

<script>
import {getCredentialList, createRobot, getStrategyTemplateList} from "../api";

export default {
  name: 'RobotCreateForm',
  data() {
    return {
      form: {
        name: '',
        credential: null,
        pair: '',
        marketType: null,
        marginCurrency: '',
        baseCurrency: '',
        quoteCurrency: '',
        targetCurrency: '',
        enable: false,
        strategyTemplate: null,
      },
      credentialOptions: [],
      strategyTemplateOptions: [],
      marketTypeOptions: [
        {
          'value': null,
          'text': '选择市场类型',
        },
        {
          'value': 'spots',
          'text': '现货',
        },
        {
          'value': 'futures',
          'text': '期货',
        },
      ],
    }
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      let data = {
        "name": this.form.name,
        "credential": this.form.credential,
        "pair": this.form.pair,
        "market_type": this.form.marketType,
        "margin_currency": this.form.marginCurrency,
        "base_currency": this.form.baseCurrency,
        "quote_currency": this.form.quoteCurrency,
        "target_currency": this.form.targetCurrency,
        "enable": this.form.enable,
        "strategy_template": this.form.strategyTemplate,
      }
      createRobot(data).then(() => {
        this.$router.push('/robot/list')
      }).catch(err => {
        console.log(err.data);
      })
    },
    setCredentialOptions(data) {
      this.credentialOptions = data.map(cred => ({value: cred.id, text: cred.note}))
    },
    setStrategyTemplateOptions(data) {
      this.strategyTemplateOptions = data.map(st => ({value: st.id, text: st.name}))
    },
  },
  mounted() {
    getCredentialList().then(response => {
      this.setCredentialOptions(response.data)
    }).catch(err => {
      this.$bvToast.toast(`无法获取交易所凭证，错误信息：${err.data || '未知错误'}`, {
        title: '数据获取失败',
        autoHideDelay: 3000,
        toaster: 'b-toaster-top-right',
        variant: 'danger',
        appendToast: false
      });
    });
    getStrategyTemplateList().then(response => {
      this.setStrategyTemplateOptions(response.data.results)
    }).catch(err => {
      this.$bvToast.toast(`无法获取策略模板，错误信息：${err.data || '未知错误'}`, {
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