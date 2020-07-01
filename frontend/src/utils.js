const userLocalStorage = {
    storageKey: 'yufu:user',
    load: function () {
        let user = JSON.parse(localStorage.getItem(this.storageKey) || 'null');
        return user || {
            userId: -1,
            username: '',
            nickname: '',
            token: '',
        }
    },
    save: function (user) {
        localStorage.setItem(this.storageKey, JSON.stringify(user))
    },
    clear: function () {
        localStorage.removeItem(this.storageKey)
    }
};

export default userLocalStorage