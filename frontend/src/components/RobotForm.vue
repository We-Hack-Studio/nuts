<template>
  <b-form @submit="onSubmit">
    <b-row>
      <b-col sm=12 md="8">
        <b-card
            header="基本设置"
            header-tag="header"
        >
          <b-row>
            <b-col sm="12" md="6">
              <b-form-group
                  label="名字:"
                  label-for="id_name"
              >
                <b-form-input
                    id="id_name"
                    v-model="form.name"
                    type="text"
                    :state="formErrors.name===undefined?null:false"
                ></b-form-input>
                <b-form-invalid-feedback :state="formErrors.name===undefined?null:false">
                  {{ formErrors.name !== undefined && formErrors.name[0] }}
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
            <b-col sm="12" md="6">
              <b-form-group
                  label="交易所凭证:"
                  label-for="id_credential"
              >
                <b-form-select
                    id="id_credential"
                    v-model="form.credential"
                    :options="credentialOptions"
                    required
                    :state="formErrors.credential===undefined?null:false"
                ></b-form-select>
                <b-form-invalid-feedback :state="formErrors.credential===undefined?null:false">
                  {{ formErrors.credential !== undefined && formErrors.credential[0] }}
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
          </b-row>
        </b-card>
        <b-card
            header="市场"
            header-tag="header"
            class="mt-3"
        >
          <b-row>
            <b-col sm="12" md="6">
              <b-form-group
                  label="市场类型:"
                  label-for="id_market_type"
              >
                <b-form-select
                    id="idMarketType"
                    v-model="form.marketType"
                    :options="marketTypeOptions"
                    required
                    :state="formErrors['market_type']===undefined?null:false"
                ></b-form-select>
                <b-form-invalid-feedback :state="formErrors['market_type']===undefined?null:false">
                  {{ formErrors['market_type'] !== undefined && formErrors['market_type'][0] }}
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
            <b-col sm="12" md="6">
              <b-form-group
                  label="交易对:"
                  label-for="id_pair"
              >
                <b-form-input
                    type="text"
                    v-model="form.pair"
                    id="id_pair"
                    :state="formErrors.pair===undefined?null:false"
                >
                </b-form-input>
                <b-form-invalid-feedback :state="formErrors.pair===undefined?null:false">
                  {{ formErrors.pair !== undefined && formErrors.pair[0] }}
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
            <!-- spots -->
            <template v-if="form.marketType==='spots'">
              <b-col sm="12" md="6">
                <b-form-group
                    label="基础币种:"
                    label-for="id_base_currency"
                    description="通常为交易对中作为资产被交易的币种。例如 BTCUSDT，基础币种为 BTC。"
                >
                  <b-form-input
                      type="text"
                      v-model="form.baseCurrency"
                      id="id_base_currency"
                      :state="formErrors['base_currency']===undefined?null:false"
                  >
                  </b-form-input>
                  <b-form-invalid-feedback :state="formErrors['base_currency']===undefined?null:false">
                    {{ formErrors['base_currency'] !== undefined && formErrors['base_currency'][0] }}
                  </b-form-invalid-feedback>
                </b-form-group>
              </b-col>
              <b-col sm="12" md="6">
                <b-form-group
                    label="计价币种:"
                    label-for="id_quote_currency"
                    description="通常为交易对中对被交易资产计价的币种。例如 BTCUSDT，计价币种为 USDT。"
                >
                  <b-form-input
                      type="text"
                      v-model="form.quoteCurrency"
                      id="id_quote_currency"
                      :state="formErrors['quote_currency']===undefined?null:false"
                  >
                  </b-form-input>
                  <b-form-invalid-feedback :state="formErrors['quote_currency']===undefined?null:false">
                    {{ formErrors['quote_currency'] !== undefined && formErrors['quote_currency'][0] }}
                  </b-form-invalid-feedback>
                </b-form-group>
              </b-col>
            </template>
            <!-- spots end -->
          </b-row>
        </b-card>
        <b-card
            header="策略"
            header-tag="header"
            class="mt-3"
        >
          <b-row>
            <b-col sm="12" md="6">
              <b-form-group
                  label="策略:"
                  label-for="id_strategy_template"
              >
                <b-form-select
                    v-model="form.strategy"
                    :options="strategyOptions"
                    id="id_strategy_template"
                    required
                    :state="formErrors.strategy===undefined?null:false"
                ></b-form-select>
                <b-form-invalid-feedback :state="formErrors.strategy===undefined?null:false">
                  {{ formErrors.strategy !== undefined && formErrors.strategy[0] }}
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
            <b-col sm="12" md="6">
              <b-form-group
                  label="目标币种:"
                  label-for="id_target_currency"
                  description="合约交易为保证金币种；现货交易为想赚取的币种。"
              >
                <b-form-input
                    type="text"
                    v-model="form.targetCurrency"
                    id="id_target_currency"
                    :state="formErrors['target_currency']===undefined?null:false"
                >
                </b-form-input>
                <b-form-invalid-feedback :state="formErrors['target_currency']===undefined?null:false">
                  {{ formErrors['target_currency'] !== undefined && formErrors['target_currency'][0] }}
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
          </b-row>
        </b-card>
      </b-col>
      <b-col sm=12 md="4">
        <div>
          <b-card title="帮助文档">
            <b-card-text>
              <a href="https://yufuquant.github.io/yufuquant-user-manual/robot/#%E5%88%9B%E5%BB%BA%E6%9C%BA%E5%99%A8%E4%BA%BA"
                 target="_blank">渔夫量化用户手册：创建机器人</a>
            </b-card-text>
          </b-card>
        </div>
        <b-button block type="submit" class="mt-3" variant="primary" :disabled="submitting">创建</b-button>
      </b-col>
    </b-row>
  </b-form>
</template>

<script>
import {createRobot} from "@/api/robot";

export default {
  name: 'RobotForm',
  props: {
    credentialOptions: {
      type: Array
    },
    strategyOptions: {
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
        baseCurrency: '',
        quoteCurrency: '',
        targetCurrency: '',
        strategy: null,
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
          'value': 'margin',
          'text': '杠杆',
        },
        {
          'value': 'linear_delivery',
          'text': '线性交割合约',
        },
        {
          'value': 'linear_perpetual',
          'text': '线性永续合约',
        },
        {
          'value': 'inverse_delivery',
          'text': '反向交割合约',
        },
        {
          'value': 'inverse_perpetual',
          'text': '反向永续合约',
        },
      ],
      submitting: false,
      formErrors: {}
    }
  },
  methods: {
    async onSubmit(event) {
      event.preventDefault()
      this.submitting = true
      let data = {
        "name": this.form.name,
        "credential": this.form.credential,
        "market_type": this.form.marketType,
        "pair": this.form.pair,
        "base_currency": this.form.baseCurrency,
        "quote_currency": this.form.quoteCurrency,
        "strategy": this.form.strategy,
        "target_currency": this.form.targetCurrency,
      }
      try {
        await createRobot(data)
        this.submitting = false
        await this.$router.push({name: 'robot-list'})
        // todo: 创建成功通知
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
            this.formErrors = error.response.data
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
        this.submitting = false
      }
    },
  },
}
</script>