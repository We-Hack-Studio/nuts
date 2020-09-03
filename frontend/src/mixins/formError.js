const formErrorMixin = {
    methods: {
        validationStateForField(field, errors) {
            let filtered = errors.filter(error => {
                const splits = error.source.pointer.split("/")
                return splits[splits.length - 1] === field
            })
            if (filtered.length !== 0) {
                return false
            }
        },
        getErrorForField(field, errors) {
            let filtered = errors.filter(error => {
                const splits = error.source.pointer.split("/")
                return splits[splits.length - 1] === field
            })
            if (filtered.length !== 0) {
                return filtered[0].detail
            }
        },
    }
}

export default formErrorMixin