<!-- <template>
  <div>
    <BBreadcrumb :items="breadcrumbs" />
    <BCard v-if="ready">
      <BListGroup>
        <BListGroupItem v-for="episode in season.episodes" :key="episode.episodeNumber">
          <BRow align-v="start" align-content="start">
            <BCol cols="5" md="4" lg="4" xl="3">
              <BImg
                fluid-grow
                class="px-2"
                width="200"
                height="200"
                blank-width="200"
                blank-height="200"
                :src="getUrl(episode.episodeNumber, episode.seasonNumber)"
                :blank-src="getUrl(episode.episodeNumber, episode.seasonNumber, true)"
              />
            </BCol>
            <BCol>
              <h4>
                {{ episode.title }}
                <RouterLink
                  class="no-link"
                  :to="getEpisodeRoute(episode.seasonNumber, episode.episodeNumber)"
                >
                  <b-icon class="h6" icon="caret-right-fill" />
                </RouterLink>
              </h4>
              <p class="pl-3">
                {{ episode.description }}
              </p>
            </BCol>
          </BRow>
        </BListGroupItem>
      </BListGroup>
    </BCard>
  </div>
</template>

<style lang="scss" scoped>
@use 'sass:color';
@use '@/scss/_variables.scss' as *;

h4 {
  .b-icon {
    font-size: 0.9rem;
    vertical-align: middle !important;
    position: relative;
    top: 3px;
    color: #007fe0;
    &:hover {
      color: color.adjust(#007fe0, $lightness: -10%);
    }
  }
}
</style>

<script lang="ts">
import { defineComponent } from 'vue'
import { BBreadcrumb, BImg } from 'bootstrap-vue-next'

export default defineComponent({
  name: 'SeasonComponent',

  components: {
    BBreadcrumb,
    BImg,
  },

  computed: {
    ready() {
      return this.$store.getters.checkPreloaded('episodes')
    },
    breadcrumbs() {
      return [
        {
          text: 'Home',
          to: { name: 'Home' },
        },
        {
          text: `Season ${this.$route.params.season}`,
          active: true,
        },
      ]
    },
    season() {
      return this.$store.state.quoteData[this.$route.params.season - 1]
    },
  },

  methods: {
    getEpisodeRoute(s, e) {
      return { name: 'Episode', params: { season: s, episode: e } }
    },
    getUrl(episode, season, thumbnail = false) {
      episode = episode.toString().padStart(2, '0')
      season = season.toString().padStart(2, '0')
      const filename = thumbnail ? 'thumbnail.jpeg' : 'full.jpeg'

      return `/img/${season}/${episode}/${filename}`
    },
  },
})
</script> -->

<script setup lang="ts"></script>
<template>
  <div>
    <h1>About</h1>
  </div>
</template>
