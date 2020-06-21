export default {
    isAuthenticated(state) {
        const token = state.user.token
        return token !== ''
    },
}