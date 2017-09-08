<style lang="scss">
    #detail ._examples{
        pre{
            overflow: hidden;
            overflow: auto;
            background-color:#fff;
            padding:10px;
            margin-top:-6px;
            max-height:6rem;
        }
    }
</style>
<style lang="scss" scoped>
    #detail{
        font-size:.14rem;
        padding-bottom:1rem;
    }
    .mytable-box{
        width:100%;
        min-width:4.6rem;
        td:nth-child(1){
            width: 150px;
            word-break: break-all;
        }
        td:nth-child(2){
            width: 150px;
            word-break: break-all;
        }
    }
    .mytable-title{
        border:1px solid #dfe6ec;
        border-bottom:0;
        padding:10px 8px;
        min-width:4.4rem;
    }
    .mytable-box .mytable-tr{
    }
    .mytable-box .mytable-tr td{
        border:1px solid #dfe6ec;
        border-right:0;
        border-bottom:0;
        padding:10px 8px;
        text-align: center;
    }
    .mytable-box .mytable-tr:last-child td{
        border-bottom:1px solid #dfe6ec;
    }
    .mytable-box .mytable-tr td:last-child{
        border-right:1px solid #dfe6ec;
        text-align:left;
    }
    #detail header section{
        margin-top:.16rem;
    }
    #detail .definition-box{
    }
    #detail .mytable-box-title{
        background-color:#eef1f6;
        td{
            border-bottom:0;
            font-weight:bold;
        }
    }
    #detail .prop-title{
        font-weight:bold;font-size:.2rem;margin-bottom:.16rem;
    }
    #detail .category-title{
        margin-top:20px;
        padding:20px 0px;
        font-weight:bold;
        background-color:#edeff0;
        font-size:16px;
    }
    #detail .more-specific-types{
        overflow:hidden;
    }
    #detail .more-specific-types li{
        float:left;
        margin:4px;
    }
    #detail ._examples{
        pre{
            overflow: hidden;
            overflow-x: auto;
        }
        .title{
            font-size:16px;
            margin-bottom:8px;
        }
        ul{
            margin-top:4px;
        }
        ul li{
            padding: 6px;
            :last-child{
                margin-top:-4px;
                padding:10px;
                background-color:#fff;
            }
        }
    }
</style>
<template>
<el-col id="detail" :span='20' :xs="{span: 24}">
    <header v-show="detailData['rdfs:label']">
        <section>
            <h4 class="prop-title" v-text="detailData['rdfs:label']"></h4>
            <span>Canonical URL: </span><a href="javascript:;" @click="goPropertiesDetail(detailData['rdfs:label'])" v-text="detailData['@id']"></a>
        </section>
        <section v-for="pathsObjs in detailData['_paths']">
            <span v-for="(pathsObj,$index) in pathsObjs['_path']">
                <a  href="javascript:;" @click="goPropertiesDetail(pathsObj['rdfs:label'])"  >{{pathsObj['rdfs:label']}}</a> <span v-if="$index != pathsObjs['_path'].length - 1 "> > </span>
            </span>
            <span v-for="(pathsObj,$index) in pathsObjs['_is_instance']">
                <a  href="javascript:;" @click="goPropertiesDetail(pathsObj['rdfs:label'])"  >{{pathsObj['rdfs:label']}}</a> 
                <span v-if="$index != pathsObjs['_path'].length - 1 "> <br/> </span>
            </span>
        </section>
        <section>
            【<span v-text="detailData['nameZh']"></span>】<span v-html="detailData['descriptionZh']"></span> <span v-html="detailData['rdfs:comment']"></span>
        </section>
        <section style="margin-bottom:.2rem;">
            Linked to schema.org:  <a href="javascript:;" target="_blank" @click="goPropertiesDetail(detailData['rdfs:label'],'schema')">http://schema.org/{{detailData['rdfs:label']}}</a>
              <span v-if="detailData['_usage']">Usage:  </span><span v-text="detailData['_usage']"></span>
        </section>

        <section style="margin-bottom:.2rem;" v-if="detailData['wikidataUrl']">
            Linked to Wikidata:  <a target="_blank" v-bind:href="detailData['wikidataUrl']">{{detailData['wikidataUrl']}} ({{detailData['wikidataName']}})</a>
        </section>

        <section style="margin-bottom:.2rem;" v-if="detailData['wikipediaUrl']">
            Linked to Wikipedia:  <a target="_blank" v-bind:href="detailData['wikipediaUrl']"  v-text="detailData['wikipediaUrl']"></a>
        </section>
    </header>

    <!--_pTree start-->
    <section style="background-color:#fff;">
        <table cellspacing="0" class="mytable-box mytable-box-title" v-if="detailData['_pTree'] && detailData['_pTree'][0]">
            <tr class="mytable-tr">
                <td>属性</td>
                <td>值域</td>
                <td style="text-align:center;">定义</td>
            </tr>
        </table>
        <section v-for="pTreeObj in detailData._pTree">
            <div class="mytable-title"> Properties from <a  href="javascript:;" @click="goPropertiesDetail(pTreeObj['rdfs:label'])" v-text="pTreeObj['rdfs:label']"></a></div>
            <table cellspacing="0" class="mytable-box">
                <tr class="mytable-tr" v-for="propertieObj in pTreeObj['_properties']">
                    <td>
                        <a  href="javascript:;" @click="goPropertiesDetail(propertieObj['rdfs:label'])" v-text="propertieObj['rdfs:label']"></a>
                    </td>
                    <td>
                        <span v-for="(rangeIncludeObj, $index) in propertieObj['rangeIncludes']">
                            <a href="javascript:;" @click="goPropertiesDetail(rangeIncludeObj['rdfs:label'])" v-text="rangeIncludeObj['rdfs:label']"></a>
                            <span v-if="propertieObj['rangeIncludes'].length -1 != $index"> or </span>
                        </span>

                        <span v-for="(rangeIncludeObj, $index) in propertieObj['domainIncludes']">
                            or <a href="javascript:;" @click="goPropertiesDetail(rangeIncludeObj['rdfs:label'])" v-text="rangeIncludeObj['rdfs:label']"></a>
                        </span>
                    </td>
                    <td>
                        <section class="definition-box">
                            【<span v-text='propertieObj["nameZh"]'></span>】
                             <span v-text='propertieObj["descriptionZh"]'></span>
                             <span v-html='propertieObj["rdfs:comment"]'></span>
                             <div v-if="propertieObj['_supersede']" style="margin-top:6px;">
                                 Supersedes: <a href="javascript:;" @click="goPropertiesDetail(propertieObj['_supersede']['rdfs:label'])" v-text="propertieObj['_supersede']['rdfs:label']"></a>
                             </div>
                             <div v-if="propertieObj['inverseOf']" style="margin-top:6px;">
                                 Inverse property: <a href="javascript:;" @click="goPropertiesDetail(propertieObj['inverseOf']['rdfs:label'])" v-text="propertieObj['inverseOf']['rdfs:label']"></a>
                             </div>
                        </section>
                    </td>
                </tr>
            </table>
        </section>
    </section>
    <!--_pTree end-->

    <!--_pRange start-->
    <section style="background-color:#fff;" v-if="detailData['_pRange'] && detailData['_pRange'][0]">
        <div class="category-title">
            {{detailData['rdfs:label']}}也可以作为下列属性的值域 
        </div>
        <table cellspacing="0" class="mytable-box mytable-box-title">
            <tr class="mytable-tr">
                <td>属性</td>
                <td>值域</td>
                <td style="text-align:center;">定义</td>
            </tr>
        </table>
        <section>
            <!-- <div class="mytable-title"> Properties from <a  href="javascript:;" @click="goPropertiesDetail(pTreeObj['rdfs:label'])" v-text="pTreeObj['rdfs:label']"></a></div> -->
            <table cellspacing="0" class="mytable-box">
                <tr class="mytable-tr" v-for="propertieObj in detailData._pRange">
                    <td>
                        <a  href="javascript:;" @click="goPropertiesDetail(propertieObj['rdfs:label'])" v-text="propertieObj['rdfs:label']"></a>
                    </td>
                    <td>
                        <span v-for="(rangeIncludeObj, $index) in propertieObj['rangeIncludes']">
                            <a href="javascript:;" @click="goPropertiesDetail(rangeIncludeObj['rdfs:label'])" v-text="rangeIncludeObj['rdfs:label']"></a>
                            <span v-if="propertieObj['rangeIncludes'].length -1 != $index"> or </span>
                        </span>

                        <span v-for="(rangeIncludeObj, $index) in propertieObj['domainIncludes']">
                            or <a href="javascript:;" @click="goPropertiesDetail(rangeIncludeObj['rdfs:label'])" v-text="rangeIncludeObj['rdfs:label']"></a>
                        </span>
                    </td>
                    <td>
                        <section class="definition-box">
                            【<span v-text='propertieObj["nameZh"]'></span>】
                             <span v-text='propertieObj["descriptionZh"]'></span>
                             <span v-html='propertieObj["rdfs:comment"]'></span>
                             <div v-if="propertieObj['_supersede']" style="margin-top:6px;">
                                 Supersedes: <a href="javascript:;" @click="goPropertiesDetail(propertieObj['_supersede']['rdfs:label'])" v-text="propertieObj['_supersede']['rdfs:label']"></a>
                             </div>
                             <div v-if="propertieObj['inverseOf']" style="margin-top:6px;">
                                 Inverse property: <a href="javascript:;" @click="goPropertiesDetail(propertieObj['inverseOf']['rdfs:label'])" v-text="propertieObj['inverseOf']['rdfs:label']"></a>
                             </div>
                        </section>
                    </td>
                </tr>
            </table>
        </section>
    </section>
    <!--_pRange end-->

    <!--rangeIncludes start-->
    <section v-if="detailData['rangeIncludes']">
        <div class="category-title">
            Values expected to be one of these types
        </div>
        <ul class="more-specific-types">
            <li v-for="_subObj in detailData['rangeIncludes']">
                <a href="javascript:;" @click="goPropertiesDetail(_subObj['rdfs:label'])" v-text="_subObj['rdfs:label']"></a>
            </li>
        </ul>
    </section>
    <!--rangeIncludes end-->

     <!--domainIncludes start-->
    <section v-if="detailData['domainIncludes']">
        <div class="category-title">
            Used on these types
        </div>
        <ul class="more-specific-types">
            <li v-for="_subObj in detailData['domainIncludes']">
                <a href="javascript:;" @click="goPropertiesDetail(_subObj['rdfs:label'])" v-text="_subObj['rdfs:label']"></a>
            </li>
        </ul>
    </section>
    <!--domainIncludes end-->

     <!--supersededBy start-->
    <section v-if="detailData['supersededBy']">
        <div class="category-title">
            SupersededBy
        </div>
        <ul class="more-specific-types">
            <li>
                <a href="javascript:;" @click="goPropertiesDetail(detailData['supersededBy']['rdfs:label'])" v-text="detailData['supersededBy']['rdfs:label']"></a>
            </li>
        </ul>
    </section>
    <!--supersededBy end-->

     <!--_supersede start-->
    <section v-if="detailData['_supersede']">
        <div class="category-title">
            Supersedes
        </div>
        <ul class="more-specific-types">
            <li v-for="_subObj in detailData['_supersede']">
                <a href="javascript:;" @click="goPropertiesDetail(_subObj['rdfs:label'])" v-text="_subObj['rdfs:label']"></a>
            </li>
        </ul>
    </section>
    <!--_supersede end-->

    <!--Sub-properties start-->
    <section v-if="detailData['_group_property'] && detailData['_sub']">
        <div class="category-title">
            Sub-properties
        </div>
        <ul class="more-specific-types">
            <li v-for="_subObj in detailData['_sub']">
                <a href="javascript:;" @click="goPropertiesDetail(_subObj['rdfs:label'])" v-text="_subObj['rdfs:label']"></a>
            </li>
        </ul>
    </section>
    <!--Sub-properties end-->

    <!--Super-properties start-->
    <section v-if="detailData['_group_property'] && detailData['_super']">
        <div class="category-title">
            Super-properties
        </div>
        <ul class="more-specific-types">
            <li v-for="_subObj in detailData['_super']">
                <a href="javascript:;" @click="goPropertiesDetail(_subObj['rdfs:label'])" v-text="_subObj['rdfs:label']"></a>
            </li>
        </ul>
    </section>
    <!--Super-properties end-->
    
    <!--_sub start-->
    <section v-if="!detailData['supersededBy'] && detailData['_group_type']  && detailData['_sub']">
        <div class="category-title">
            More specific Types
        </div>
        <ul class="more-specific-types">
            <li v-for="_subObj in detailData['_sub']">
                <a href="javascript:;" @click="goPropertiesDetail(_subObj['rdfs:label'])" v-text="_subObj['rdfs:label']"></a>
            </li>
        </ul>
    </section>
    <!--_sub end-->

    <!--_instances start-->
    <section v-if="detailData['_instances']">
        <div class="category-title">
            Enumeration members
        </div>
        <ul class="more-specific-types">
            <li v-for="_subObj in detailData['_instances']">
                <a href="javascript:;" @click="goPropertiesDetail(_subObj['rdfs:label'])" v-text="_subObj['rdfs:label']"></a>
            </li>
        </ul>
    </section>
    <!--_instances end-->

    <!--_source start-->
    <section v-if="detailData['_source']">
        <div class="category-title">
            Source
        </div>
        <ul>
            <li v-for="_sourceObj in detailData['_source'] " v-html="_sourceObj['rdfs:comment']" style="margin-bottom:8px;"></li>
        </ul>
    </section>
    <!--_source end-->

    <!--_sourceAck start-->
    <section v-if="detailData['_sourceAck'] && detailData['_sourceAck']">
        <div class="category-title">
            Acknowledgement
        </div>
        <ul>
            <li v-for="_sourceAckObj in detailData['_sourceAck'] " v-html="_sourceAckObj['rdfs:comment']" style="margin-bottom:8px;"></li>
        </ul>
    </section>
    <!--_sourceAck end-->

    <!--_examples start new-->
    <section v-if="detailData['_examples']" class="_examples">
        <div class="category-title">
            Examples
        </div>
        <section v-for="(_examplesObj,$index) in detailData['_examples']" :key='$index'>
            <div class="title">example{{$index + 1}}</div>
            <el-tabs v-model="exampleFirst" type="card">
                <el-tab-pane label="Without Markup" name="without-markup">
                    <pre v-text="_examplesObj['PRE-MARKUP']"></pre>
                </el-tab-pane>
                <el-tab-pane label="Microdata" :name="microdata">
                    <pre v-text="_examplesObj['MICRODATA']"></pre>
                </el-tab-pane>
                <el-tab-pane label="RDFa" name="rdfa">
                    <pre v-text="_examplesObj['RDFA']"></pre>
                </el-tab-pane>
                <el-tab-pane label="JSON-LD" name="json-ld">
                    <pre v-text="_examplesObj['JSON']"></pre>
                </el-tab-pane>
            </el-tabs>
        </section>
    </section>

    <!--_examples start end-->

    <!--_examples start-->
   <!--  <section v-if="detailData['_examples']" class="_examples">
        <div class="category-title">
            Examples
        </div>
        <section v-for="(_examplesObj,$index) in detailData['_examples']">
            <div class="title">example{{$index + 1}}</div>
            <div class="title" style="margin-top:6px;">Without Markup Microdata RDFa JSON-LD</div>
            <ul>
                <li><pre v-text="_examplesObj['PRE-MARKUP']"></pre></li>
                <li><pre v-text="_examplesObj['MICRODATA']"></pre></li>
                <li><pre v-text="_examplesObj['RDFA']"></pre></li>
                <li><pre v-text="_examplesObj['JSON']"></pre></li>
            </ul>
        </section>
    </section> -->
    <!--_examples end-->

    <!--version start-->
    <p v-if="detailData['_version']" style="margin-top:30px;" class="version"><b>Schema Version {{detailData["_version"]}}</b>  The original definition of this concept is from 
        <a href="http://schema.org">http://schema.org</a>.
    </p>
    <!--version end-->

    <p style="font-size:16px;text-align:center;margin-top:.4rem;color:#aaa;" v-if="!detailData['_version']">加载中......</p>

</el-col>
</template>

<script>
    export default {
        name: 'keepAlive',
        data: () => {
            return {
                detailData: {},
                oldQuery:"000000",
                exampleFirst: "without-markup"
            }
        },
        watch: {
          $route: function(now,old){
            let main = this.$ele('.main_body');
            main.scrollTop = 0;
            if(this.$isProd()){
                this.getTableData(now.path.substr(1));
            }else{
                this.getTableData('temp-two');
            }
          }
        },
        mounted(){
            if(this.$isProd()){
                this.getTableData(this.$route.params.query);
            }else{
                this.getTableData('temp-one');
            }
        },
        methods: {
            goPropertiesDetail(prop,type) {
                if(type == 'schema'){
                    window.location.href = 'http://schema.org/' + prop;
                }
                this.$router.push({name: 'detail',params: {query: prop}});
            },
            getTableData(propFile) {
                if(this.$isProd()){
                    this.$http.get('http://cnschema.org/data/'+ propFile +'.json').then(ret => {
                        this.detailData = ret.body;
                    })
                }else{
                    this.$http.get('/static/'+ propFile +'.json').then(ret => {
                        this.detailData = ret.body;
                    })
                }
            }
        }
    }
</script>










