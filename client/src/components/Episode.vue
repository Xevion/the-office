<template>
    <div>
        <b-card :title="`Season ${this.$route.params.season} Episode ${this.$route.params.episode} \
        - ${episode != null ? episode.title : ''}`" class="mb-4">
            <span v-if="episode">
                {{ episode.description }}
            </span>
            <CharacterList v-if="episode && episode.characters" :characters="episode.characters"></CharacterList>
        </b-card>
        <div v-if="episode != null">
            <b-card v-for="(scene, sceneIndex) in episode.scenes" :key="`scene-${sceneIndex}`"
                    class="mb-1" body-class="p-0">
                <b-card-text class="my-2">
                    <QuoteList :quotes="scene.quotes" :sceneIndex="sceneIndex"></QuoteList>
                    <span v-if="scene.deleted" class="mt-n2 mb-4 text-muted deleted-scene pl-2"
                          :footer="`Deleted Scene ${scene.deleted}`">
                                  Deleted Scene {{ scene.deleted }}
                              </span>
                </b-card-text>
            </b-card>
        </div>
    </div>
</template>

<style lang="scss">
.card-title {
    font-family: 'Montserrat', sans-serif;
    font-weight: 600;
}

.deleted-scene {
    font-size: 0.75em;
    line-height: 12px;
}
</style>

<script>
import axios from 'axios';
import QuoteList from './QuoteList.vue';
import CharacterList from './CharacterList.vue';

export default {
  name: 'Episode',
  components: {
    QuoteList,
    CharacterList,
  },
  data() {
    return {
      episode: null,
    };
  },
  methods: {
    getEpisode() {
      const path = `${process.env.VUE_APP_BASE_APP_URL}/api/episode/\
${this.$route.params.season}/${this.$route.params.episode}/`;
      axios.get(path)
        .then((res) => {
          this.episode = res.data;
          // Scroll
          if (this.$route.hash) {
            this.$nextTick(() => {
              const section = document.getElementById(this.$route.hash.substring(1));
              this.$scrollTo(section, 500, { easing: 'ease-in' });
            });
          }
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
