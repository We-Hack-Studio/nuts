export default {
    SET_USER: (state, payload) => {
        state.user = {...payload}
    },
    REMOVE_USER: (state) => {
        state.user = {
            userId: -1,
            username: '',
            nickname: '',
        }
    },
    SET_AUTH_TOKEN: (state, authToken) => {
        state.authToken = authToken
    },
    REMOVE_AUTH_TOKEN: (state) => {
        state.authToken = ""
    },
}