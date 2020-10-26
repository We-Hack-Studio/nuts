<template>
    <b-form>
        <b-form-group v-for="field in fields" :key="field.code" :label="field.name" :description="field.description">
            <component
                v-if="getInputType(field) === 'number'"
                v-model.number="form[field.code]"
                v-bind:is="fieldFactory(field.type)"
                :items="field.items"
                type="number"
            ></component>
            <component
                v-else
                v-model="form[field.code]"
                v-bind:is="fieldFactory(field.type)"
                :items="field.items"
            ></component>
        </b-form-group>
    </b-form>
</template>

<script>
import { BFormCheckbox, BFormInput } from 'bootstrap-vue';
import SelectItem from './ParamFormSelectItem';

export default {
    name: 'parameter-form',
    props: {
        fields: Array,
    },
    mounted() {
        this.initForm();
    },
    data() {
        return {
            form: {},
            strategyTemplateOptions: [],
        };
    },
    components: { BFormInput },

    methods: {
        getInputType(field) {
            if (field.type === 'float' || field.type === 'integer') {
                return 'number';
            }
            return 'text';
        },
        initForm() {
            this.fields.forEach(item => {
                this.$set(this.form, item.code, item.value);
                // this.$set(this.form, item.code, 1);
            });
        },
        fieldFactory: function(fieldType) {
            switch (fieldType) {
                case 'boolean':
                    return BFormCheckbox;
                case 'integer':
                case 'float':
                    return BFormInput;
                case 'enum':
                    return SelectItem;
                default:
                    return BFormInput;
            }
        },
    },
};
</script>

<style scoped>
fieldset {
    margin-bottom: 1rem;
    padding: 0;
    border: 0;
}
</style>
