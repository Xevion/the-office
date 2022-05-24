<template>
    <b-card>
        <template v-if="ready">
            <h4>
                The Office Quotes
            </h4>
            <b-card-text>
                A Vue.js application serving you 54,000+ quotes from your
                favorite show - The Office.
                <br>
                Click on a Season and Episode on the left-hand sidebar to view quotes.
                Search for quotes with the instant searchbox.
                <br>
                This site is going through a big update & re-model, so the homepage isn't quite ready.
                However, as of the time of writing this, most everything else is setup.
                <hr>
                <p style="text-align: center">
                    Check out the <router-link :to="{'name': 'About'}">
                        about page
                    </router-link> for more info on what this website is.
                </p>
            </b-card-text>
        </template>
        <b-card-text v-else>
            <Skeleton style="width: 45%" />
            <Skeleton style="width: 75%" />
            <Skeleton style="width: 60%" />
            <Skeleton style="width: 60%" />
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
    computed: {
        ready() {
            return true;
            // return this.stats != null;
        }
    },
    created() {
        // this.getStats();
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
};
</script>
