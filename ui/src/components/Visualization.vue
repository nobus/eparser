<template>
  <div class="visualization">
    <!--<h1>visualization</h1>-->
    <HChart 
      v-if="loaded"
      :chartdata="chartdata"
    />
  </div>
</template>

<script>
import HChart from './HChart.vue'

export default {
    name: 'Visualization',
    components: {
        HChart,
    },
    data: () => ({
        loaded: false,
        chartdata: null,
    }),
    async mounted () {
        this.loaded = false
        try {
            const resp = await fetch('/etsy_api/hgram')
            this.chartdata = await resp.json()
            this.loaded = true
        } catch (e) {
            console.error(e)
        }
    }
}
</script>

<style scoped>
.visualization {
    position: relative;
    background: rgb(214, 210, 210);
    grid-column: 1;
    grid-row: 1;
}

.chart rect {
  fill: steelblue;
}

.chart text {
  fill: white;
  font: 10px sans-serif;
  text-anchor: end;
}
</style>
