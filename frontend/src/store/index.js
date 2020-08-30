import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations'
import getters from "./getters";

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        authToken: "",
        user: {
            "username": "",
            "userId": -1,
            "nickname": "",
        }
    },
    mutations,
    getters,
})

export default store