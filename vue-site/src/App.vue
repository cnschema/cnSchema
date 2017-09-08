<template>
  <div id="app">
  <!-- <keep-alive include="keepAlive"> -->
    <router-view name='header'></router-view>
    <el-col class='main_body' :offset='4' :span='20' :xs="{span:'24',offset:'0'}">
        <keep-alive include="keepDicAlive">
          <router-view name='main'></router-view>
        </keep-alive>
    </el-col>
    <router-view name='footer'></router-view>
  </div>
</template>

<script>
import 'normalize.css';
export default {
  name: 'app'
}
</script>

<style>
    @import 'assets/css/common.css'
</style>
