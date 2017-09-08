<template>
<header id="header">
    <el-menu theme="dark" class="el-menu-demo" mode="horizontal" :router='true' :default-active='active' @select='judge'>
      <el-menu-item index="/index" class='desk'>cnSchema</el-menu-item>
      <li class='el-menu-item'>
        <a href="https://github.com/cnschema/cnschema" target="_blank">项目</a>
      </li>
      <li class='el-menu-item'>
        <a href="https://github.com/cnschema/cnschema/wiki" target="_blank">文档</a>
      </li>
      <el-menu-item index="/_cns_vocab">词汇表</el-menu-item>
      <el-menu-item index="/_cns_about/aboutus">关于</el-menu-item>
      <li class='el-menu-item'>
        <a href="http://openkg.cn" target="_blank">OpenKG.CN</a>
      </li>
      <li id="search_item_all" class="search_item list-item" v-if='show'>
        <my-search @enter='enter' sID='headerSID'></my-search>
      </li>
    </el-menu>
    <i class='el-icon-arrow-left goback' @click='goback'></i>
    <i class='el-icon-search search' @click='gosearch'></i>
    <h1 class='header_title'>{{title}}</h1>
    <my-list></my-list>
</header>
</template>

<script>
  export default {
    name: 'keepAlive',
    data(){
      return {
        show: true,
        title: '',
        active: '',
      }
    },
    mounted(){
      this.judge()
    },
    methods: {
      judge(path = this.$route.path){
        let href;
        this.show = true;
        switch(path){
          case '/':
            this.show = false;
            this.title = 'cnSchema';
            path = '/index';
          break;
          case '/index':
            this.show = false;
            break;
          case '/_cns_about/aboutus':
            this.title = '关于';
            break;
          case '/_cns_about/people':
            path = '/_cns_about/aboutus';
            this.title = '关于';
            break;
          case '/_cns_about/contacts':
            path = '/_cns_about/aboutus';
            this.title = '关于';
            break;
          case '/_cns_vocab':
            this.title = '词汇表';
            break;
          default: 
            this.title = path.substr(1);
        }
        this.active = path;
      },
      enter(query){
        this.$router.push({name: 'desk',params: {enter: true,query}})
        this.show = false;
        let desk = this.$ele('.desk');
        desk.click();
      },
      goback(){
        this.$router.go(-1);
      },
      gosearch(){
        this.$router.push({name:'desk'})
      },
    },
    watch: {
      $route(now,old){
        this.judge(now.path);
      }
    }
  }
</script>

<style scoped lang='scss'>
.nav-menu-skip{
   display:inline-block;
   padding:0 .1rem;
}
.nav-menu-skip:hover{
  text-decoration:none;
}
#header{
    height: .6rem;
}
.el-menu-demo{
    display: flex;
    flex: 1;
    padding-left: 16%;
    .is-active{
      color: #20a0ff !important;
    }
}
.el-menu-item{
  color: #fff;
  a{
    text-decoration: none;
    display: block;
    height: 100%;
  }
}
.search_item{
  position: absolute;
  right: .16rem;
  width: 3rem;
}
.list-item{
  line-height: 60px;
  font-size: 14px;
  padding: 0 20px;
  transition: border-color .3s,background-color .3s,color .3s;
  white-space: nowrap;
  margin: 0;
}
.header_title,.goback,.search{
  display: none;
}

@media screen and (max-width: 768px) {
  #header{
    background: #324057;
    height: .4rem;
    line-height: .4rem;
    text-align: center;
  }
  .header_title{
    color: #fff;
    display: block;
    font-size: .16rem;
    font-family: sans-serif;
    margin-top: 0px;
  }
  .el-menu-demo{
      display: none;
  }
  .goback,.search{
    position: absolute;
    display: block;
    font-size: .2rem;
    top: .1rem;
    color: #fff;
  }
  .goback{
    left: .1rem;
  }
  .search{
    right: .15rem;
  }
}
</style>
