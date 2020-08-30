const storage = {
    storageKeyPrefix: 'yufuquant:',
    loadUser: function () {
        let user = JSON.parse(localStorage.getItem(this.storageKeyPrefix + 'user') || 'null');
        return user || {
            userId: -1,
            username: '',
            nickname: '',
        }
    },
    saveUser: function (user) {
        localStorage.setItem(this.storageKeyPrefix + 'user', JSON.stringify(user))
    },
    loadAuthToken: function () {
        return localStorage.getItem(this.storageKeyPrefix + 'auth-token') || ''
    },
    saveAuthToken: function (authToken) {
        localStorage.setItem(this.storageKeyPrefix + 'auth-token', authToken)
    },
    clear: function () {
        localStorage.removeItem(this.storageKeyPrefix + 'user')
        localStorage.removeItem(this.storageKeyPrefix + 'auth-token')
    }
};

export default storage