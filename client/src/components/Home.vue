<template>
    <b-card>
        <template v-if="stats">
            <h4>
                The Office Quotes
            </h4>
            <b-card-text>
                A Vue.js application serving you {{ stats.totals.quote }} quotes from your
                favorite show - The Office.
                <br/>
                Click on a Season and Episode on the left-hand sidebar to view quotes.
                Search for quotes with the instant searchbox.
            </b-card-text>
        </template>
        <b-card-text v-else>
            <Skeleton style="width: 45%"></Skeleton>
            <Skeleton style="width: 75%"></Skeleton>
            <Skeleton style="width: 60%"></Skeleton>
            <Skeleton style="width: 60%"></Skeleton>
        </b-card-text>
    </b-card>
</template>

<script>
import axios from "axios";
import Skeleton from './Skeleton.vue';

export default {
    name: "Home",
    components: {
        Skeleton
    },
    data() {
        return {
            stats: null,
        };
    },
    methods: {
        getStats() {
            const path = `${process.env.VUE_APP_API_URL}/api/stats/`;
            axios
                .get(path)
                .then((res) => {
                    this.stats = res.data;
                })
                .catch((error) => {
                    // eslint-disable-next-line no-console
                    console.error(error);
                });
        },
    },
    created() {
        this.getStats();
    },
};
</script>
