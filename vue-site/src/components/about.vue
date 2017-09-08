<template>
<div id="about">
    <el-row>
        <h1 class='head'></h1>
    </el-row>
    <el-row class='about_body'>
        <el-col :span='3' class='menu_body'>
            <el-menu :default-active="myactive" theme='dark' class="el-menu-vertical" :collapse="true" @select='change'>
              <el-menu-item index="aboutus">
                关于我们
              </el-menu-item>
              <el-menu-item index="people">
                人员
              </el-menu-item>
              <el-menu-item index="contacts">
                联络和合作
              </el-menu-item>
            </el-menu>
        </el-col>
        <el-col :span='16' :offset='1' class='about_main' :xs="{span:22}">
            <router-view></router-view>
        </el-col>
    </el-row>
</div>
</template>

<script>
  export default {
    data() {
      return {
        myactive: 'aboutus',
      }
    },
    methods: {
        change(path) {
            this.$router.push({name: path})
            let a = this.$eles('a');
            Array.prototype.forEach.call(a,(ele) => {
                ele.setAttribute('target','_blank')
            })
        },
        log(){
            console.log(1)
        }
    },
    mounted() {
        let a = this.$eles('a');
        Array.prototype.forEach.call(a,(ele) => {
            ele.setAttribute('target','_blank')
        })
        let last = this.$route.path.lastIndexOf('/');
        let path = this.$route.path.substr(last + 1);
        this.myactive = path;
    },
    watch: {
        $route: function(now){
            let last = now.path.lastIndexOf('/');
            let path = now.path.substr(last + 1);
            this.myactive = path;
        }
    }
  }
</script>

<style lang='scss'>
#about{
    display: flex;
    flex-direction: column;
    height: 90%;
    min-height: 400px;
    .about_body{
        display: flex;
        flex: 1;
    }
    .menu_body{
        background: #324057;
    }
    .el-menu-vertical{
        width: 100%;
    }
    .el-menu-item{
        color: #fff;
        font-size: .16rem;
    }
    .is-active{
        color: #20a0ff !important;
    }
    .about_mobile_list{
        display: none;
    }
    .br{
        line-height: 0;
        margin: 0;
    }
    a{
        color: #3f93d2;
    }
    dl{
        font-size: .3rem;
        dd,dt{
            display: inline-block;
            font-size: .16rem;
        }
    }
    h1{
        font-size: .2rem;
        margin: .1rem 0;
        color: #509ec7;
    }
    p{
        text-indent: 2em;
        font-size: .16rem;
        line-height: .3rem;
        margin: .12rem 0;
        color: #384840;
    }
    address{
        font-size: .22rem;
        margin-top: 20px;
    }
}

@media screen and (max-width: 768px){
    #about{
        flex: 1;
    }
    .menu_body{
        display: none;
    }
    .head{
        display: none;
    }
    .about_mobile_list{
        display: block;
    }
    h1,address{
        font-size: .2rem;
        text-align: center;
        margin: .1rem 0;
    }
    p{
        word-break: break-all;
        font-size: .14rem;
    }
}
</style>




