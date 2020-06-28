<template>
  <div>
    <div class="d-flex justify-content-end">
      <b-icon-arrow-clockwise class="mr-3" @click="refreshGridList"></b-icon-arrow-clockwise>
      <b-icon-gear class="mr-3" v-b-modal.grid-params-form-modal></b-icon-gear>
      <b-icon-trash class="mr-3" variant="danger" @click="showMsgBox" v-if="hasGrids"></b-icon-trash>
    </div>
    <b-table hover :items="gridList" :fields="fields" class="mt-2" :tbody-tr-class="holdingClass"
             small>
      <template v-slot:cell(gridIndex)="data">
        {{ data.value + 1 }}
      </template>
      <template v-slot:cell(qty)="data">
        {{ data.item.filledQty }}/{{ data.item.entryQty }}
      </template>
    </b-table>
    <b-modal button-size="sm" size="sm" id="grid-params-form-modal" centered title="网格参数设置">
      <b-form @submit="onSubmit">
        <b-form-group
                label="最低价:"
                label-for="id_min_price"
        >
          <b-form-input
                  id="id_min_price"
                  v-model="form.minPrice"
                  type="number"
                  required
          ></b-form-input>
        </b-form-group>
        <b-form-group label="最高价:" label-for="id_max_price">
          <b-form-input
                  id="id_max_price"
                  v-model="form.maxPrice"
                  type="number"
                  required
          ></b-form-input>
        </b-form-group>
        <b-form-group label="网格数量:" label-for="id_num_grids">
          <b-form-input
                  id="id_num_grids"
                  v-model="form.numGrids"
                  type="number"
                  required
          ></b-form-input>
        </b-form-group>
        <b-form-group label="投入本金:" label-for="id_principal">
          <b-form-input
                  id="id_principal"
                  v-model="form.principal"
                  type="number"
                  required
          ></b-form-input>
        </b-form-group>
        <b-form-group label="最大杠杆:" label-for="id_leverage">
          <b-form-input
                  id="id_leverage"
                  v-model="form.maxLeverage"
                  type="number"
                  required
          ></b-form-input>
        </b-form-group>
        <b-form-group label="止盈间距:" label-for="id_take_profit_range">
          <b-form-input
                  id="id_take_profit_range"
                  v-model="form.takeProfitRange"
                  type="number"
                  required
          ></b-form-input>
        </b-form-group>
      </b-form>
      <template v-slot:modal-footer="{ok}">
        <b-button size="sm" variant="primary" @click="onSubmit(ok, $event)">
          确认
        </b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
    import {createGrids, clearGrids} from "../api";

    export default {
        props: {
            gridList: Array
        },
        data() {
            return {
                form: {
                    minPrice: null,
                    maxPrice: null,
                    numGrids: null,
                    principal: null,
                    maxLeverage: null,
                    takeProfitRange: null,
                },
                fields: [
                    {
                        key: 'gridIndex',
                        label: '层'
                    },
                    {
                        key: 'entryPrice',
                        label: '入场价'
                    },
                    {
                        key: 'exitPrice',
                        label: '出场价'
                    },
                    {
                        key: 'qty',
                        label: '已成交/数量'
                    },
                    // {
                    //     key: 'action',
                    //     label: '操作'
                    // }
                ],
            }
        },
        methods: {
            refreshGridList() {
                this.$emit('refresh-grids')
            },
            onSubmit(ok, evt) {
                evt.preventDefault()
                let data = {
                    "min_price": this.form.minPrice,
                    "max_price": this.form.maxPrice,
                    "num_grids": this.form.numGrids,
                    "principal": this.form.principal,
                    "max_leverage": this.form.maxLeverage,
                    "take_profit_range": this.form.takeProfitRange,
                }
                createGrids(this.$route.params.id, data).then(() => {
                    this.form = {
                        minPrice: null,
                        maxPrice: null,
                        numGrids: null,
                        principal: null,
                        maxLeverage: null,
                        takeProfitRange: null,
                    }
                    this.$emit('grids-created')
                    ok()
                }).catch(err => {
                    console.log(err.data);
                })
            },
            clearGridTable() {
                clearGrids(this.$route.params.id).then(() => {
                    this.$emit('grids-cleared')
                }).catch(err => {
                    console.log(err.data);
                })
            },
            showMsgBox() {
                this.$bvModal.msgBoxConfirm('清除网格将取消交易所全部挂单并重置交易机器人状态，如果当前账户仍有持仓，请登录交易所手动平仓后再设置新的网格。', {
                    title: '确认清除？',
                    size: 'sm',
                    buttonSize: 'sm',
                    okVariant: 'danger',
                    okTitle: '确认',
                    cancelTitle: '取消',
                    footerClass: 'p-2',
                    hideHeaderClose: false,
                    centered: true
                })
                    .then(value => {
                        if (!value) {
                            return
                        }
                        this.clearGridTable()
                    })
                    .catch(err => {
                        console.log(err);
                        // An error occurred
                    })
            },
            holdingClass(item, type) {
                if (!item || type !== 'row') return
                if (item.holding) return 'text-success'
                if (item.filledQty > 0) return 'text-warning'
            }
        },
        computed: {
            hasGrids() {
                return this.gridList.length > 0
            }
        }
    }
</script>