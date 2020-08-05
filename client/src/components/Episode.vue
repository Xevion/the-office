<template>
    <div>
        <b-card :title="`Season ${this.$route.params.season} Episode ${this.$route.params.episode} \
        - ${episode != null ? episode.title : ''}`" class="mb-4">
            <span v-if="episode">
                {{ episode.description }}
            </span>
        </b-card>
        <b-card v-for="(scene, scene_index) in episode.scenes" :key="`scene-${scene_index}`"
                class="mb-1" body-class="pb-0">
            <b-card-text>
                <QuoteList :quotes="scene.quotes"></QuoteList>
            </b-card-text>
        </b-card>
    </div>
</template>

<script>
import axios from 'axios';
import QuoteList from './QuoteList.vue';

export default {
  name: 'Episode',
  components: { QuoteList },
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
