<template>
    <el-col id="dictionary" :span='20' :xs="{span: 24}">
      <el-tabs v-model="nodeQuery" @tab-click="handleClick">
        <el-tab-pane label="Classes（分类列表）" name="classesName">
              <el-input
                placeholder="输入关键字进行过滤"
                v-model="filterText">
              </el-input>
              <el-tree
                class="filter-tree"
                :data="clssesDatas"
                :props="defaultProps"
                :empty-text="loadTips"
                default-expand-all
                :filter-node-method="filterNode"
                @node-click="goClassesDetail"
                ref="tree2"
                empty-text='正在加载中...'
                ></el-tree>
        </el-tab-pane>
        <el-tab-pane label="Properties（属性列表）" name="propertiesName">
              <template>
                  <el-table
                    :data="propertieDatas"
                    border
                    style="width: 100%;">
                    <el-table-column
                      :width="attrWidth"
                      label="属性">
                      <template scope="scope">
                        <a href="javascript:;" @click="goPropertiesDetail(scope.row['rdfs:label'])" v-text="scope.row['rdfs:label']"></a>
                      </template>
                    </el-table-column>
                    <el-table-column
                       label="定义">
                      <template scope="scope">
                        【<span v-html='scope.row.nameZh'></span>】 <span v-html='scope.row.descriptionZh'></span>
                          <span v-html='scope.row["rdfs:comment"]'></span>
                      </template>
                    </el-table-column>
                  </el-table>
                </template>
        </el-tab-pane>
      </el-tabs>
    </el-col>
</template>
<script>
  import { Loading } from 'element-ui';
  export default {
    name: 'keepDicAlive',
    data() {
      return {
        filterText: '',
        nodeQuery:'classesName',
        clssesDatas:[],
        propertieDatas:[],
        loadTips: '加载中......',
        defaultProps: {
          children: 'children',
          label: function(data, node){
             return data.name + "(" + data.nameZh + ")";
          }
        },
        attrWidth: 100,
        loading: false
      };
    },
    watch: {
      filterText(val) {
        this.$refs.tree2.filter(val);
      }
    },
    mounted(){
        this.getTreeData()
    },
    created(){
      let width = window.innerWidth;
      if(width > 768){
        this.attrWidth = 200;
      }
    },
    methods: {
      goClassesDetail(data,node){
        this.$router.push({name: 'detail',params: {query: data.name}})
      },
      goPropertiesDetail(prop){
        this.$router.push({name: 'detail',params: {query: prop}})
      },
      handleClick(current_tab){
          if(current_tab.name == 'propertiesName' && this.propertieDatas.length == 0){
              if(this.$isProd()){
                    this.$http.get('http://cnschema.org/data2/properties.json').then(ret => {
                        this.propertieDatas = ret.body;
                    })
                }else{
                    this.$http.get('/static/properties.json').then(ret => {
                        this.propertieDatas = ret.body;
                    })
                }
          }
      },
      filterNode(value, data) {
        if (!value) return true;
        return data.name.indexOf(value) !== -1 || data.nameZh.indexOf(value) !== -1 ;
      },getTreeData(){
            if(this.$isProd()){
                  this.$http.get('http://cnschema.org/data2/classes.json').then(ret => {
                      this.clssesDatas = [ret.body];
                  })
              }else{
                   this.$http.get('/static/classes.json').then(ret => {
                        this.clssesDatas = [ret.body];
                    })
              }
      }
    }
  };
</script>

<style scoped lang="scss">
  #dictionary{
    font-size:.16rem;
    .el-tree.filter-tree{
          margin-top: .14rem;
    }
  }
</style>

