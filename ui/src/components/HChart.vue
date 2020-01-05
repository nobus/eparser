
<script>

import { Bar } from 'vue-chartjs'

export default {
    name: 'HChart',
    extends: Bar,
    props: {
        chartdata: {
            type: Object,
            default: null,
        },
    },
    mounted () {
        this.renderChart(
            this.chartdata,
            {
                maintainAspectRatio: false,
                scales: {
                    yAxes: [{type: 'logarithmic'}]
                }
            }
        )
    }
}

</script>