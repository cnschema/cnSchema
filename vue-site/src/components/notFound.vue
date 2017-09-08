<template>
<el-col id="notFound" class="active" :span='20' :xs='{span:24}'>
    <img src="../assets/img/page-not-found.png" alt="404 not found" title='404 not found' class="image clip">
</el-col>
</template>

<style scoped>
    #notFound{
        height: 80%;
    }
    .clip[style] {
        opacity: 0;
    }
    .active .clip:not([style]) {
        opacity: 0;
        animation: fadeIn .1s .4s both;
    }
    .active .clip[style] {
        will-change: transform;
        animation: noTransform .5s both;
    }
    .image{
        position: absolute;
        top: 15%;
        left: 50%;
        /*待优化*/
        margin-left: -242.5px;
    }
    @keyframes noTransform {
        to {
            opacity: 1;
            transform: translate3d(0, 0, 0) rotate(0);
        }
    }
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    @media screen and (max-width: 768px){
        .image{
            zoom: .7;
        }
    }
</style>

<script>
    export default {
        name: 'keepAlive',
        methods: {
            clipPath(t){
                if(!t){return false}t.removeAttribute("id");var r={height:t.clientHeight,width:t.clientWidth,distance:60,html:t.outerHTML};if(window.getComputedStyle(document.body).webkitClipPath){var a=r.distance,n=r.width,e=r.height;var o="";for(var i=0;i<n;i+=a){for(var h=0;h<e;h+=a){var d=[i,h],u=[i,h+a],l=[i+a,h+a],v=[i+a,h];var c=[i+a/2,h+a/2];var m=[[d,c,v],[d,u,c],[c,u,l],[v,c,l]];m.forEach(function(t,a){var n=t.map(function(t){return t.map(function(t){return t+"px"}).join(" ")}).join();var e="-webkit-clip-path: polygon("+n+");";var i=Math.random();var h=i<.5?-1:1;var u=[600*(.5-Math.random()),600*(.5-Math.random())];var l="translate("+u.map(function(t){return t+"px"}).join()+") rotate("+Math.round(h*360*Math.random())+"deg)";var v="-webkit-transform:"+l+";transform:"+l+";";o=o+r.html.replace('">','" style="'+e+v+'">')})}}t.parentNode.innerHTML=r.html+o;return true}else{t.className+=" no-clipath";return false}
            }
        },
        mounted() {
            if(window.innerWidth > 768){
                this.clipPath(this.$ele('img'));
            }
        }
    }
</script>

