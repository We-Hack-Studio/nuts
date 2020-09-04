import {Formatter} from "sarala-json-api-data-formatter";


const formatterMixin = {
    data: function () {
        return {
            formatter: new Formatter()
        }
    }
}
export default formatterMixin