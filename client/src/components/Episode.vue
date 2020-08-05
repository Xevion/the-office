<template>
    <div>
        <b-card :title="`Season ${this.$route.params.season} Episode ${this.$route.params.episode}`" class="mb-4">
            <span v-if="episode">
                {{ episode.description }}
            </span>
        </b-card>
        <b-card v-for="(scene) in episode.scenes" :key="scene.text" class="mb-1" body-class="pb-0">
            <b-card-text>
                <p v-for="quote in scene.quotes" :key="quote.text">
                    <strong>{{ quote.speaker }}</strong>: {{ quote.text }}
                </p>
            </b-card-text>
        </b-card>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Episode',
  data() {
    return {
      episode: null,
    };
  },
  methods: {
    getEpisode() {
      const path = `http://localhost:5000/api/episode/${this.$route.params.season}/${this.$route.params.episode}/`;
      axios.get(path)
        .then((res) => {
          this.episode = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.error(error);
        });
    },
  },
  created() {
    this.getEpisode();
  },
  watch: {
    $route() {
      this.getEpisode();
    },
  },
};
</script>
