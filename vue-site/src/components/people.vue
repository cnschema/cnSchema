<template>
<div class="people">
    <h1 class='starter'>cnSchema发起人</h1>
    <dl>
        <template v-for='people in peoples'>
            <dd style="width:80px;">{{people.name}}</dd>
            <dt>{{people.info}}</dt>
            <p class="br"><br></p>
        </template>
    </dl>
    <h1 class='contor'>cnSchema贡献者</h1>
    <dl>
        <template v-for='people in contributer'>
            <dd> {{people.name}}&nbsp;&nbsp;</dd>
        </template>
    </dl>
</div>
</template>

<script>
    export default{
        name: 'keepAlive',
        data(){
            return {
                peoples: [{
                    name: '丁力',
                    info: '海知智能 CTO/博士'
                },{
                    name: '陈华钧',
                    info: '浙江大学   教授'
                },{
                    name: '漆桂林',
                    info: '东南大学   教授'
                },{
                    name: '王昊奋',
                    info: '乐言科技   CTO/博士'
                },{
                    name: '谢殿侠',
                    info: '海知智能  CEO'
                },{
                    name: '李涓子',
                    info: '清华大学  教授'
                },{
                    name: '闫俊',
                    info: '医渡云  首席人工智能科学家'
                },{
                    name: '肖仰华',
                    info: '复旦大学  教授'
                },{
                    name: '鲍捷',
                    info: '文因互联  CEO/博士'
                },{
                    name: '曾毅',
                    info: '中科院自动化所 研究员'
                },{
                    name: 'Jeff Pan',
                    info: '英国阿伯丁大学  教授'
                },],
                contributer: [{
                    name: '邹磊(北京大学)'
                },{
                    name: '于彤(中国中医科学院信息研究所)'
                },{
                    name: '张鹏(清华大学)'
                },{
                    name: '李金龙(招商银行)'
                },{
                    name: '钟艳琴(招商银行)'
                },{
                    name: '徐波(东华大学)'
                },{
                    name: '侯磊(清华大学)'
                },{
                    name: '胡伟(南京大学)'
                },{
                    name: '吴天星(东南大学)'
                },{
                    name: '徐常亮(新华智云)'
                },{
                    name: '张大卫(微软亚洲研究院)'
                },{
                    name: '徐艺(微软亚洲研究院)'
                },{
                    name: '仲亮靓(东南大学)'
                },{
                    name: '王梁(浙江大学)'
                },{
                    name: '张宇轩(浙江大学)'
                },{
                    name: '邓淑敏(浙江大学)'
                },{
                    name: '王宇(海知智能)'
                },{
                    name: '杨平京(海知智能)'
                },{
                    name: '孙娜(海知智能)'
                },{
                    name: '陈旭(海知智能)'
                },{
                    name: '董孙竑路'
                },{
                    name: '郭唯'
                  },{
                      name: '杜宁林'
                },{
                    name: 'Kevin Xin'
                }]
            }
        }
    }
</script>

<style lang='scss' scoped>
    .people{
        h1{
            font-size: .2rem;
            color: #509ec7;
        }
        .starter,.contor{
            margin-bottom: 0 !important;
        }
        .contor{
            margin-top: .25rem !important;
        }
        dt{
            color: #826565;
        }
        dd{
            color: #667279;
            margin-right: .1rem;
        }
    }
    @media screen and (max-width: 768px) {
        .people{
            text-align: center;
        }
    }
</style>
