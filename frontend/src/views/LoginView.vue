<template>
    <div class="fixed-top fixed-bottom login-page">
        <b-row>
            <b-col sm="12" md="6" lg="4" offset-md="3" offset-lg="4">
                <b-card class="p-lg-3">
                    <div class="title py-4 text-secondary">
                        <b-icon icon="x-diamond" scale="3" class="mr-4" />
                        <h4>渔夫量化</h4>
                    </div>
                    <div class="text-center small text-secondary py-4 mb-2">使用账号密码登录</div>
                    <b-form @submit="onSubmit">
                        <b-alert :show="errors.length > 0" variant="danger">
                            <ul class="pl-2">
                                <li class="small" v-for="(error, index) in errors" :key="index">{{ error.detail }}</li>
                            </ul>
                        </b-alert>
                        <b-form-group>
                            <b-input-group class="input-group" size="lg">
                                <b-input-group-prepend class="prepend-class">
                                    <b-icon icon="person-fill"></b-icon>
                                </b-input-group-prepend>
                                <b-form-input
                                    class="input-class"
                                    id="id_username"
                                    v-model="form.username"
                                    type="用户名"
                                    placeholder=""
                                    required
                                ></b-form-input>
                            </b-input-group>
                        </b-form-group>
                        <b-form-group>
                            <b-input-group class="input-group" size="lg">
                                <b-input-group-prepend class="prepend-class">
                                    <b-icon icon="key-fill"></b-icon>
                                </b-input-group-prepend>
                                <b-form-input
                                    class="input-class"
                                    placeholder="密码"
                                    id="id_password"
                                    v-model="form.password"
                                    type="password"
                                    required
                                ></b-form-input>
                            </b-input-group>
                        </b-form-group>
                        <b-button
                            size="lg"
                            class="mt-5 mb-4"
                            type="submit"
                            block
                            variant="primary"
                            :disabled="formProcessing"
                            >登录</b-button
                        >
                    </b-form>
                </b-card>
            </b-col>
        </b-row>
    </div>
</template>

<script>
import { postAuthLogin } from '@/api';
import storage from '../utils';
import { Formatter } from 'sarala-json-api-data-formatter';

export default {
    data() {
        return {
            form: {
                username: '',
                password: '',
            },
            errors: [],
            formProcessing: false,
            formatter: new Formatter(),
        };
    },
    methods: {
        async login(username, password) {
            const type = 'tokens';
            const data = this.formatter.serialize({ type, username, password });
            return await postAuthLogin(data);
        },

        async onSubmit(event) {
            this.formProcessing = true;
            event.preventDefault();
            try {
                const loginRes = await this.login(this.form.username, this.form.password);
                const result = this.formatter.deserialize(loginRes.data);

                const authToken = result['auth_token'];
                this.$store.commit('SET_AUTH_TOKEN', authToken);
                storage.saveAuthToken(authToken);

                const userData = result.user.data;
                const user = {
                    userId: userData.id,
                    username: userData.username,
                    nickname: userData.nickname,
                };
                this.$store.commit('SET_USER', user);
                storage.saveUser(user);

                this.formProcessing = false;

                await this.$router.push({ name: 'robot-list' });
            } catch (error) {
                if (error.response) {
                    if (error.response.status >= 500) {
                        this.$bvToast.toast('服务端错误', {
                            title: '登录失败',
                            autoHideDelay: 3000,
                            toaster: 'b-toaster-top-center',
                            variant: 'danger',
                            appendToast: false,
                        });
                    } else if (error.response.status >= 400) {
                        // form validation error
                        this.errors = error.response.data.errors;
                    }
                } else {
                    this.$bvToast.toast(error.message, {
                        title: '登录失败',
                        autoHideDelay: 3000,
                        toaster: 'b-toaster-top-center',
                        variant: 'danger',
                        appendToast: false,
                    });
                }
                this.$store.commit('REMOVE_AUTH_TOKEN');
                this.$store.commit('REMOVE_USER');
                storage.clear();
                this.formProcessing = false;
            }
        },
    },
};
</script>

<style scoped lang="scss">
.login-page {
    background: linear-gradient(150deg, #98aaff 0%, #0270e6 100%);
    // background: linear-gradient(180deg, #4e73df 10%, #224abe 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    .row {
        width: 100%;
    }
}
.title {
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom: 1px solid #eee;
}
.form-group {
    margin-bottom: 2rem;
}
.card-body {
    padding: 36px;
}
.input-group {
    // box-shadow: 0 2px 12px rgba($color: #000000, $alpha: 0.1);
    box-shadow: 0 1px 3px rgba(50, 50, 93, 0.15), 0 1px 0 rgba(0, 0, 0, 0.02);
    color: #adb5bd;
    .prepend-class {
        width: 46px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    .input-class {
        border: none;
        font-size: 1rem;
        line-height: 1.5;
        color: $secondary;
    }
}
</style>
