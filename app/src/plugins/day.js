import 'dayjs/locale/ja'
import dayjs from 'dayjs'
import Vue from 'vue'

dayjs.locale('ja')

export default ({ app }, inject) => {
    inject('dayjs', ((string) => dayjs(string)))
}