import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations'
import getters from "./getters";
import userLocalStorage from "../utils";

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        user: userLocalStorage.load()
    },
    mutations,
    getters,
})

export default store