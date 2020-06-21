export default {
    SET_USER: (state, payload) => {
        state.user = {...payload}
    },
    REMOVE_USER: (state) => {
        state.user = {
            userId: -1,
            username: '',
            nickname: '',
            token: '',
        }
    }
}