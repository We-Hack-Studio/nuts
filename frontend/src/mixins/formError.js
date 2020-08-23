const formErrorMixin = {
    methods: {
        validationStateForField(field, errors) {
            let filtered = errors.filter(error => {
                return error['field'] === field
            })
            if (filtered.length !== 0) {
                return false
            }
        },
        getErrorForField(field, errors) {
            let filtered = errors.filter(error => {
                return error['field'] === field
            })
            if (filtered.length !== 0) {
                return filtered[0].message
            }
        },
    }
}

export default formErrorMixin