<template>
  <BCard>
    <template v-if="ready">
      <h4>The Office Quotes</h4>
      <BCardText>
        A Vue.js application serving you 54,000+ quotes from your favorite show - The Office.
        <br />
        Click on a Season and Episode on the left-hand sidebar to view quotes. Search for quotes
        with the instant searchbox.
        <br />
        This site is going through a big update & re-model, so the homepage isn't quite ready.
        However, as of the time of writing this, most everything else is setup.
        <hr />
        <p style="text-align: center">
          Check out the <RouterLink :to="{ name: 'About' }"> about page </RouterLink> for more info
          on what this website is.
        </p>
      </BCardText>
    </template>
    <BCardText v-else>
      <Skeleton style="width: 45%" />
      <Skeleton style="width: 75%" />
      <Skeleton style="width: 60%" />
      <Skeleton style="width: 60%" />
    </BCardText>
  </BCard>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import axios from 'axios'
import Skeleton from './Skeleton.vue'
import { BCardText, BCard } from 'bootstrap-vue-next'

export default defineComponent({
  name: 'HomeComponent',

  components: {
    Skeleton,
    BCardText,
    BCard,
  },

  data() {
    return {
      stats: null,
    }
  },

  computed: {
    ready() {
      return true
      // return this.stats != null;
    },
  },

  created() {
    // this.getStats();
  },

  methods: {
    getStats() {
      const path = `${import.meta.env.VUE_APP_API_URL}/api/stats/`
      axios
        .get(path)
        .then((res) => {
          this.stats = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    },
  },
})
</script>
