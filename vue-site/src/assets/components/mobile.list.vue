<template>
    <div class="mobile-list" :class='status'>
        <div class="list-item" :name='name' v-for='name in names' @click='goPages(name)'></div>
        <div class="list" @click.self='toggleMenu'></div>
    </div>
</template>

<script>
    export default {
        data(){
            return {
                status: 'close',
                names: ['desk','dictionary','aboutus']
            }
        },
        methods: {
            toggleMenu(){
                this.status = this.status == 'close' ? 'open' : 'close'
            },
            goPages(name){
                console.log(1)
                this.$router.push({name});
                this.status = 'close';
            }
        }
    }
</script>

<style scoped>
    .mobile-list{
        position: fixed;
        font-size: .16rem;
        border-radius: 50%;
        height: 25px;
        width: 25px;
        background: #bce2ff;
        bottom: 70px;
        left: 50px;
        z-index: 1;
    }
    .list-item,.list{
        width: 100%;
        height: 100%;
        overflow: hidden;
        border-radius: 50%;
        position: absolute;
        background: #ccc;
        transition: all .3s linear;
        will-change: left,top;
    }
    .close .list-item{
        left: 0;
        top: 0;
    }
    .open .list-item:nth-child(1){
        left: -15px;
        top: -55px;
    }
    .open .list-item:nth-child(2){
        left: 40px;
        top: -45px;
    }
    .open .list-item:nth-child(3){
        left: 55px;
        top: 7px;
    }

    @media screen and (min-width: 768px) {
        .mobile-list{
            display: none;
        }
    }
</style>







