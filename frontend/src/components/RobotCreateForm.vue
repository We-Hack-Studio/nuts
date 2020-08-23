<template>
  <b-form @submit="onSubmit">
    <b-form-group
        label="名字:"
        label-for="id_name"
    >
      <b-form-input
          id="id_name"
          v-model="form.name"
          type="text"
          :state="validationStateForField('name', formErrors)"
      ></b-form-input>
      <b-form-invalid-feedback :state="validationStateForField('name', formErrors)">
        {{ getErrorForField('name', formErrors) }}
      </b-form-invalid-feedback>
    </b-form-group>

    <b-form-group
        label="交易所凭证:"
        label-for="id_credential"
    >
      <b-form-select
          id="id_credential"
          v-model="form.credential"
          :options="credentialOptions"
          required
          :state="validationStateForField('credential', formErrors)"
      ></b-form-select>
      <b-form-invalid-feedback :state="validationStateForField('credential', formErrors)">
        {{ getErrorForField('credential', formErrors) }}
      </b-form-invalid-feedback>
    </b-form-group>

    <b-form-group
        label="交易对:"
        label-for="id_pair"
    >
      <b-form-input
          type="text"
          v-model="form.pair"
          id="id_pair"
          :state="validationStateForField('pair', formErrors)"
      >
      </b-form-input>
      <b-form-invalid-feedback :state="validationStateForField('pair', formErrors)">
        {{ getErrorForField('pair', formErrors) }}
      </b-form-invalid-feedback>
    </b-form-group>

    <b-form-group
        label="市场类型:"
        label-for="id_market_type"
    >
      <b-form-select
          id="idMarketType"
          v-model="form.marketType"
          :options="marketTypeOptions"
          required
          :state="validationStateForField('market_type', formErrors)"
      ></b-form-select>
      <b-form-invalid-feedback :state="validationStateForField('market_type', formErrors)">
        {{ getErrorForField('market_type', formErrors) }}
      </b-form-invalid-feedback>
    </b-form-group>

    <!-- spots -->
    <template v-if="form.marketType==='spots'">
      <b-form-group
          label="基础币种:"
          label-for="id_base_currency"
          description="通常为交易对中作为资产被交易的币种。例如 BTCUSDT，基础币种为 BTC。"
      >
        <b-form-input
            type="text"
            v-model="form.baseCurrency"
            id="id_base_currency"
            :state="validationStateForField('base_currency', formErrors)"
        >
        </b-form-input>
        <b-form-invalid-feedback :state="validationStateForField('base_currency', formErrors)">
          {{ getErrorForField('base_currency', formErrors) }}
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
          label="计价币种:"
          label-for="id_quote_currency"
          description="通常为交易对中对被交易资产计价的币种。例如 BTCUSDT，计价币种为 USDT。"
      >
        <b-form-input
            type="text"
            v-model="form.quoteCurrency"
            id="id_quote_currency"
            :state="validationStateForField('quote_currency', formErrors)"
        >
        </b-form-input>
        <b-form-invalid-feedback :state="validationStateForField('quote_currency', formErrors)">
          {{ getErrorForField('quote_currency', formErrors) }}
        </b-form-invalid-feedback>
      </b-form-group>
    </template>
    <!-- spots end -->

    <b-form-group
        label="目标币种:"
        label-for="id_target_currency"
        description="合约交易为保证金币种；现货交易为想赚取的币种。"
    >
      <b-form-input
          type="text"
          v-model="form.targetCurrency"
          id="id_target_currency"
          :state="validationStateForField('target_currency', formErrors)"
      >
      </b-form-input>
      <b-form-invalid-feedback :state="validationStateForField('target_currency', formErrors)">
        {{ getErrorForField('target_currency', formErrors) }}
      </b-form-invalid-feedback>
    </b-form-group>
    <b-form-group
        label="策略模板:"
        label-for="id_strategy_template"
    >
      <b-form-select
          v-model="form.strategyTemplate"
          :options="strategyTemplateOptions"
          id="id_strategy_template"
          required
          :state="validationStateForField('strategy_template', formErrors)"
      ></b-form-select>
      <b-form-invalid-feedback :state="validationStateForField('strategy_template', formErrors)">
        {{ getErrorForField('strategy_template', formErrors) }}
      </b-form-invalid-feedback>
    </b-form-group>
    <b-form-group
        label="启用:"
        label-for="id_enable"
    >
      <b-form-checkbox
          id="id_enable"
          v-model="form.enable"
          name="enable"
          value=true
          unchecked-value=false
          :state="validationStateForField('enabled', formErrors)"
      >
      </b-form-checkbox>
      <b-form-invalid-feedback :state="validationStateForField('enabled', formErrors)">
        {{ getErrorForField('enabled', formErrors) }}
      </b-form-invalid-feedback>
    </b-form-group>
    <b-button block type="submit" variant="primary" class="mt-3" :disabled="formProcessing">创建</b-button>
  </b-form>
</template>

<script>
import {createRobot} from "@/api";
import formErrorMixin from "@/mixins/formError"

export default {
  name: 'RobotCreateForm',
  mixins: [formErrorMixin],
  props: {
    credentialOptions: {
      type: Array
    },
    strategyTemplateOptions: {
      type: Array
    },
  },
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
      formProcessing: false,
      formErrors: []
    }
  },
  methods: {
    async onSubmit(evt) {
      this.formProcessing = true
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
        "enabled": this.form.enable,
        "strategy_template": this.form.strategyTemplate,
      }
      try {
        await createRobot(data)
        this.formProcessing = false
        await this.$router.push({name: 'robot-list'})
      } catch (error) {
        if (error.response) {
          if (error.response.status === 500) {
            this.$bvToast.toast('服务端错误', {
              title: '机器人创建失败',
              autoHideDelay: 3000,
              toaster: 'b-toaster-top-center',
              variant: 'danger',
              appendToast: false
            });
          } else if (error.response.status === 400) {
            // form validation error
            this.formErrors = error.response.data.errors
          }
        } else {
          this.$bvToast.toast(error.message, {
            title: '机器人创建失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        }
        this.formProcessing = false
      }
    },
  },
}
</script>