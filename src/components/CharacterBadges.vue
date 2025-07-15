<template>
  <div v-if="characters" class="pt-2" :fluid="true">
    <BButton
      v-for="(character, character_id) in characters"
      :id="`character-${character_id}`"
      :key="character.name"
      squared
      class="mx-2 my-1 character-button"
      size="sm"
      :title="`${character.appearances} Quote${character.appearances > 1 ? 's' : ''}`"
      :to="{ name: 'Character', params: { character: character_id } }"
    >
      {{ character.name }}
      <BBadge class="ml-1">
        {{ character.appearances }}
      </BBadge>
    </BButton>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { BButton, BBadge } from 'bootstrap-vue-next'

export default defineComponent({
  components: {
    BButton,
    BBadge,
  },

  props: {
    characters: {
      type: Object,
      required: true,
    },
  },
})
</script>
