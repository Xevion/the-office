<template>
  <table class="quote-list w-100 px-3">
    <tr
      v-for="(quote, index) in quotes"
      :id="`${sceneIndex}-${index}`"
      :key="`quote-${index}`"
      :class="
        $route.hash !== null && $route.hash.substring(1) === `${sceneIndex}-${index}`
          ? 'highlight'
          : ''
      "
    >
      <td v-if="quote.speaker" class="quote-speaker pl-3">
        <DynamicSpeaker
          v-if="quote.isAnnotated"
          :text="quote.speaker"
          :characters="quote.characters"
          class="my-3"
        />
        <NuxtLink
          v-else
          :to="{ name: 'Character', params: { character: quote.character } }"
          class="speaker-link"
        >
          {{ quote.speaker }}
        </NuxtLink>
      </td>
      <!-- eslint-disable-next-line vue/no-v-html -->
      <td class="quote-text w-100 pr-3" v-html="transform(quote.text)" />
      <td class="px-1 pl-2">
        <a :href="quote_link(index)" class="no-link" @click="copy(index)">
          <!-- <b-icon icon="link45deg" /> -->
        </a>
      </td>
    </tr>
  </table>
</template>

<script lang="ts">
// import { defineComponent } from 'vue';

// import DynamicSpeaker from '@/components/features/DynamicSpeaker.vue';

// export default defineComponent({
//   components: {
//     DynamicSpeaker,
//   },

//   props: {
//     sceneIndex: {
//       required: true,
//       type: Number,
//     },
//     quotes: {
//       required: true,
//       type: Array,
//     },
//   },

//   methods: {
//     transform(quoteText) {
//       if (quoteText.includes('[')) {
//         return quoteText.replace(/\[([^\]]+)]/g, ' <i>[$1]</i> ');
//       }
//       return quoteText;
//     },
//     quote_link(quoteIndex) {
//       return `/${this.$route.params.season}/${this.$route.params.episode}#${this.sceneIndex}-${quoteIndex}`;
//     },
//     copy(quoteIndex) {
//       this.$copyText(import.meta.env.VUE_APP_BASE_URL + this.quote_link(quoteIndex));
//     },
//   },
// });
</script>

<style lang="scss">
@use '@/scss/_variables.scss' as *;

.speaker-bg {
  color: $gray-100;
}

.speaker-link {
  &,
  &:hover {
    color: $gray-100;
    cursor: pointer;
    text-decoration: none;
  }
}
</style>
