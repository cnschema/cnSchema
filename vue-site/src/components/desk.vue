<template>
<el-col id="main" :span='20' :xs="{span: 24}">
    <my-search @enter='enter' searchClass='search-input-body'></my-search>
    <div class="container">
      <p class='tip' v-if='tip'>{{tip}}</p>
      <div v-for='ret of showResult' class="ret">
        <h3><a @click="goDetail(ret['@id'])" href='javascript:void(0)'>{{ret.name}}({{ret.nameZh}}) </a></h3>
        <p>
            {{ret.description}}({{ret.descriptionZh}})
        </p>
        <a @click="goDetail(ret['@id'])" href='javascript:void(0)'>{{ret['@id']}}</a>
      </div>
      <div class="introduction" v-if='!tip && !total'>
        <h1>欢迎访问cnSchema.org</h1>
        <p>
          cnSchema.org是一个基于社群的数据标准，结合中文特定应用场景的应用需求，我们连接了schema.org，WikiData等开放数据接口标准，为中文领域的知识图谱，聊天机器人，网页开发等在线服务提供数据接口标准。
        </p>
        <router-link to='/_cns_vocab'>开始使用</router-link>
      </div>
    </div>
    <el-pagination
      class='pages'
      layout="prev, pager, next"
      :total="total"
      :page-size='pageSize'
      @current-change='changePage'
      v-if='total'
      ></el-pagination>
      <br/><br/>
</el-col>
</template>

<script>
  export default {
    name: 'keepAlive',
    data(){
      return {
        total: '',
        pageSize: 10,
        showResult: [],
        tip: '',
        currentQuery:"",
        height: 400,
      }
    },
    mounted(){
      if(this.$route.params.enter){
        this.enter(this.$route.params.query,1);
      }
      let container = this.$ele('.container');
      this.height = container.offsetHeight - 70;
    },
    methods: {
      enter(query,currentPage) {
        if(query == ''){
          this.tip = '请输入搜索内容'
          return;
        }
        if(!currentPage){
          currentPage = 1;
        }
        this.currentQuery = query;
        var offset = (currentPage - 1) * this.pageSize;
        this.$http.get(`${this.$host.auto_api}/search?q=${query}&offset=${offset}`).then(ret => {
          this.showResult = ret.data.results;
          this.total = ret.data.total;
          if(this.total == 0){
            this.tip = '您要搜索的内容不存在'
          }else{
            this.tip = ''
          }
        })
        this.setPadding(0);
      },
      changePage(currentPage){
        this.enter(this.currentQuery, currentPage);
      },
      goDetail(url){
        let lastIndex = url.lastIndexOf('/');
        let query = url.substr(lastIndex + 1);
        this.$router.push({name: 'detail',params: {query}})
      },
      setPadding(px = 0){
        let main = this.$ele('#main');
        main.style.paddingTop = px + 'px';
      }
    }
  }
</script>

<style scoped lang='scss'>
  #main{
    display: flex;
    flex-direction: column;
    flex: 1;
    font-size: .14rem;
    padding-top: 100px;
  }
  .container{
    flex: 1;
  }
  .pages {
    display: flex;
    margin: .15rem 0;
    align-self: center;
  }
  .tip {
    font-size: .2rem;
    font-family: cursive;
    color: #ad7272;
  }
  .ret:first-child{
    margin-top:0rem;
  }
  .ret{
    display: flex;
    flex-direction: column;
    margin: .22rem 0;
    *{margin: 0;}
    h3{
      font-size: .16rem;
      a{
        color: #213147;
      }
    }
    p{
      font-size: .14rem;
      margin: .07rem 0;
      color: #616161;
    }
    a{
      text-decoration: none;
    }
  }
  .introduction{
    *{color: #2480a0;}
    h1{font-size: .18rem;margin-top: .5rem;}
    p{font-size: .16rem;margin: .25rem 0;text-indent: 1.3em;line-height: .3rem;}
    a{text-decoration: underline;}
  }

@media screen and (max-width: 768px){
  #main{
    padding-top: 0;
  }
  .container{
    width: 90%;
    margin: 0 auto;
    margin-top: .3rem;
  }
  .ret{
    h3{font-size: .16rem;}
    p{font-size: .14rem;}
  }
  .introduction{
    h1{
      margin-top: 0;
      font-size: .16rem;
      text-align: center;
    }
    p{
      margin: .15rem 0;
    }
    p,a{
      font-size: .14rem;
    }
  }
}
</style>









