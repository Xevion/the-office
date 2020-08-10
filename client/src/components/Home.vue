<template>
    <b-card title="The Office Quotes">
        <b-card-text>
            A Vue.js application serving you {{ stats.totals.quote }} quotes from your favorite show - The Office.
            <br>
            Click on a Season and Episode on the left-hand sidebar to view quotes.
            Search for quotes with the instant searchbox.
        </b-card-text>
    </b-card>
</template>

<style>
    .card {
        color: #b3b3b3;
        background-color: #161616;
        border-bottom: 1px solid rgba(0, 0, 0, 0.88);
        border-radius: 0;
    }
</style>

<script>
import axios from 'axios';

export default {
  name: 'Home',
  data() {
    return {
      stats: null,
    };
  },
  methods: {
    getStats() {
      const path = `${process.env.VUE_APP_BASE_APP_URL}/api/stats/`;
      axios.get(path)
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
