import search from './search.vue';
import mobile_list from './mobile.list.vue';
import footer from './footer.vue';

const myComponents = {
    install: Vue => {
        Vue.component('my-search',search);
        Vue.component('my-list',mobile_list);
        Vue.component('my-footer',footer);
    }
}

export default myComponents;