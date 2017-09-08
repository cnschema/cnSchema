import axios from 'axios'
const util = {
    install: Vue => {
        Vue.prototype.$http = axios;
        Vue.prototype.$host = {
            localhost: 'http://localhost:8081/',
            detail_api: 'http://cnschema.org/data',
            auto_api: 'http://cnschema.org:18080'
        },
        Vue.prototype.$isProd = () => {
            if(window.location.href.indexOf('cnschema.org') > -1){
                return true;
            }
            return false;
        },
        Vue.prototype.$event = {
            add: (ele,type,cb) => {
                if(window.addEventListener){
                    ele.addEventListener(type,cb)
                }else{
                    ele.attachEvent('on' + type,cb)
                }
                let e = window.evnet;
                cb.call(this,e)
            },
            remove: (ele,type,fn) => {
                if(window.addEventListener){
                    ele.removeEventListener(type,fn)
                }else{
                    ele.detachEvent('on' + type,fn)
                }
            }
        },
        Vue.prototype.$ele = (selector) => {
            return document.querySelector(selector);
        },
        Vue.prototype.$eles = (selector) => {
            return document.querySelectorAll(selector);
        }
    }
}
export default util
