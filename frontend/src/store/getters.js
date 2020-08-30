export default {
    isAuthenticated(state) {
        return state.authToken !== ''
    },
}