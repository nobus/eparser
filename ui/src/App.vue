<template>
  <div id="app">
    <Visualization />
    <UrlList />
    <Options />
  </div>
</template>

<script>
import Visualization from './components/Visualization.vue'
import Options from './components/Options.vue'
import UrlList from './components/UrlList.vue'

export default {
    name: 'App',
    components: {
        Visualization,
        Options,
        UrlList,
    },
}
</script>

<style>
#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 6px;
    display: grid;
    grid-template-columns: 3fr 1fr;
    grid-template-rows: 2fr 1fr ;
    grid-gap: 10px;
}
</style>
