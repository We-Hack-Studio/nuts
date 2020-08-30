import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations'
import getters from "./getters";
import storage from "../utils";

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        authToken: storage.loadAuthToken(),
        user: storage.loadUser()
    },
    mutations,
    getters,
})

export default store