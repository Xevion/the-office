<template>
  <span>
    <template v-for="(constituent, index) in texts">
      <RouterLink
        class="speaker-link"
        v-if="constituent.route"
        :key="index"
        :to="constituent.route"
      >
        {{ constituent.text }}
      </RouterLink>
      <span class="speaker-bg" v-else :key="'plain-' + index">{{ constituent }}</span>
    </template>
  </span>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'DynamicSpeaker',

  props: {
    text: { type: String, required: true },
    characters: { type: Object, required: true },
  },

  computed: {
    texts() {
      return this.text.split(/({[^}]+})/).map((item) => {
        const id = item.substring(1, item.length - 1);
        if (item.startsWith('{'))
          return {
            text: this.characters[id],
            route: {
              name: 'Character',
              params: { character: id },
            },
          };
        else return item;
      });
    },
  },
});
</script>

<style scoped></style>
