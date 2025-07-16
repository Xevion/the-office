<script setup lang="ts">
import QuoteList from '@/components/features/QuoteList.vue';
// import CharacterBadges from '@/components/features/CharacterBadges.vue';
import Skeleton from '@/components/common/Skeleton.vue';
import Breadcrumb from '@/components/common/Breadcrumb.vue';
import { computed } from 'vue';

const route = useRoute();

const params = { season: 1, episode: route.params.id };

const breadcrumbs = computed(() => {
  return [
    { text: 'Home', to: '/' },
    { text: `Season ${params.season}`, to: `/season/${params.season}` },
    {
      text: `Episode ${params.episode}`,
      to: `/episode/${params.episode}`,
    },
  ];
});

// export default defineComponent({
//   name: 'EpisodeComponent',

//   components: {
//     QuoteList,
//     CharacterBadges,
//     Skeleton,
//     BBreadcrumb,
//   },

//   computed: {
//     episode() {
//       return this.$store.getters.getEpisode(this.params.season, this.params.episode);
//     },
//     // Shorthand - literally useless, why does everything to have such long prefixes in dot notation
//     params() {
//       return this.$route.params;
//     },
//     ready() {
//       return this.$store.getters.isFetched(this.params.season, this.params.episode);
//     },
//     breadcrumbs() {
//       return [
//         {
//           text: 'Home',
//           to: {
//             name: 'Home',
//           },
//         },
//         {
//           text: `Season ${this.$route.params.season}`,
//           to: {
//             name: 'Season',
//             season: this.$route.params.season,
//           },
//         },
//         {
//           text: `Episode ${this.$route.params.episode}`,
//           to: {
//             name: 'Episode',
//             season: this.$route.params.season,
//             episode: this.$route.params.episode,
//           },
//           active: true,
//         },
//       ];
//     },
//   },

//   watch: {
//     // When route changes, fetch data for current Episode route
//     $route() {
//       nextTick(() => {
//         this.fetch();
//       });
//     },
//   },

//   created() {
//     // When page loads directly on this Episode initially, fetch data
//     this.fetch();
//   },

//   methods: {
//     async fetch() {
//       // Fetch the episode, then scroll - already fetched episode should scroll immediately
//       this.$store
//         .dispatch(types.FETCH_EPISODE, { season: this.params.season, episode: this.params.episode })
//         .then(() => {
//           // Force update, as for some reason it doesn't update naturally. I hate it too.
//           this.$forceUpdate();

//           // Scroll down to quote
//           if (this.$route.hash) {
//             nextTick(() => {
//               const section = document.getElementById(this.$route.hash.substring(1));
//               this.$scrollTo(section, 500, { easing: 'ease-in' });
//             });
//           }
//         });
//     },
//   },
// });
</script>

<template>
  <div class="h-full w-full p-4">
    <Breadcrumb :items="breadcrumbs" />
    <!-- <BCard v-else class="breadcrumb-skeleton mb-3">
      <Skeleton style="width: 40%" />
    </BCard> -->
    <!-- <BCard class="mb-4">
      <template v-if="ready">
        <h3 class="card-title">"{{ episode.title }}"</h3>
        <span>{{ episode.description }}</span>
        <CharacterBadges v-if="episode && episode.characters" :characters="episode.characters" />
      </template>
      <template v-else>
        <Skeleton style="width: 30%" />
        <Skeleton style="width: 70%; height: 60%" />
        <Skeleton style="width: 45%; height: 60%" />
        <Skeleton style="width: 69%; height: 40%" />
      </template>
    </BCard> -->
    <!-- <div v-if="ready">
      <BCard
        v-for="(scene, sceneIndex) in episode.scenes"
        :key="`scene-${sceneIndex}`"
        class="mb-1"
        body-class="p-0"
      >
        <BCardText class="my-2">
          <QuoteList :quotes="scene.quotes" :scene-index="sceneIndex" />
          <span
            v-if="scene.deleted"
            class="mt-n2 text-muted deleted-scene mb-4 pl-2"
            :footer="`Deleted Scene ${scene.deleted}`"
          >
            Deleted Scene {{ scene.deleted }}
          </span>
        </BCardText>
      </BCard>
    </div> -->
  </div>
</template>

<style lang="scss">
.card-title {
  font-family: 'Montserrat', sans-serif;
  font-weight: 500;
}

.deleted-scene {
  font-size: 0.75em;
  line-height: 12px;
}
</style>
