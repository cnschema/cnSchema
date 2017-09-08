<template>
    <el-autocomplete
      :id='sID'
      :class="searchClass"
      v-model="search"
      class='search-input'
      :fetch-suggestions="querySearch"
      placeholder='输入概念分类，属性。如 "人"'
      @select="handleSelect"
      icon='close'
      :on-icon-click='clearSearch'
      :trigger-on-focus="false"
    ></el-autocomplete>
</template>

<script>
    export default {
        props: {
          sID: {
            type: String,
            default: 'mysID'
          },
          searchClass: {
            default: 'search-input-header'
          }
        },
        data() {
          return {
            search: '',
          }
        },
        methods: {
          querySearch(queryString, cb) {
            this.$http.get(`${this.$host.auto_api}/autocomplete?q=${queryString}`).then((ret) => {
              let data = ret.data.results;
              data.forEach((ele,index) => {
                ele.value = ele.name + '(' + ele.nameZh + ')';
              })
              cb(data);
            })
          },
          handleSelect(item) {
            let href = item['@id'];
            let lastIndex = href.lastIndexOf('/');
            let query = href.substr(lastIndex + 1);
            this.$router.push({name: 'detail',params: {query}})
            this.search = '';
          },
          clearSearch() {
            this.search = '';
          },
          keydown(e){
            try{
              if(e.keyCode == 13){
                let suggests = this.$eles('.el-autocomplete-suggestion');
                Array.prototype.forEach.call(suggests,suggest => {
                  suggest.style.display = 'none';
                })
                this.$emit('enter',this.search);
              }
            }catch(e){}
          }
        },
        mounted(){
            let query = `#${this.sID} .el-input__inner`;
            let searchInput = this.$ele(query);
            let path = this.$route.path;
            this.$event.remove(searchInput,'keydown',this.keydown);
            this.$event.add(searchInput,'keydown',this.keydown);
        }
    }
</script>

<style scoped>
.search-input-body{
  margin: .2rem 0;
}
.search-input-header{
  width: 300px;
  position: absolute;
  right: 0px;
}
@media screen and (max-width: 768px){
    .search-input{
      display: flex;
      margin: 20px auto;
      width: 90%;
    }
}
</style>

<style>
.search-input-header .el-input__inner{
  background: #EFF2F7;
}
</style>





