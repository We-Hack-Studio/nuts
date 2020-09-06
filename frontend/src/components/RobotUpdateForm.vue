<template>
  <b-card class="mt-2">
    <b-form @submit="onSubmit">
      <b-form-row>
        <b-col md="12">
          <label>名字</label>
        </b-col>
        <b-col md="12">
          <b-form-input type="text" v-model="form.name"></b-form-input>
        </b-col>
      </b-form-row>
      <b-form-row class="mt-2">
        <b-col md="12">
          <label>启用</label>
        </b-col>
        <b-col md="12">
          <b-form-checkbox id="id_enable" v-model="form.enable" name="enable" value="true" unchecked-value="false">
          </b-form-checkbox>
        </b-col>
      </b-form-row>
      <b-button block type="submit" variant="primary" class="mt-3">更新</b-button>
    </b-form>
  </b-card>
</template>

<script>
import { getRobotsId, patchRobotsId } from '../api';
import formatterMixin from '@/mixins/formatter';

export default {
  name: 'RobotUpdateForm',
  mixins: [formatterMixin],
  data() {
    return {
      form: {
        name: '',
        enable: false,
        strategyTemplate: null,
      },
      strategyTemplateOptions: [],
    };
  },
  computed: {
    robotId() {
      return this.$route.params.id;
    },
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      let data = {
        name: this.form.name,
        enable: this.form.enable,
      };
      patchRobotsId(this.robotId, this.formatter.serialize({ type: 'robots', id: this.robotId, ...data }))
        .then(() => {
          this.$router.push(`/robot/${this.robotId}`);
        })
        .catch(err => {
          console.log(err.data);
        });
    },
    initRobotForm(data) {
      this.form = {
        name: data.name,
        enabled: data.enabled,
      };
    },

    async getRobotsId() {
      try {
        const response = await getRobotsId(this.robotId);
        this.initRobotForm(this.formatter.deserialize(response.data));
      } catch (err) {
        this.$bvToast.toast(`无法更新机器人数据，错误信息：${err.data || '未知错误'}`, {
          title: '数据更新失败',
          autoHideDelay: 3000,
          toaster: 'b-toaster-top-right',
          variant: 'danger',
          appendToast: false,
        });
      }
    },
  },
  mounted() {
    this.getRobotsId();
  },
};
</script>
