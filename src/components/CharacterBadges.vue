<template>
    <div class="pt-2" v-if="characters" :fluid="true">
        <b-button squared class="mx-2 my-1 character-button" size="sm" v-for="(character, character_id) in characters"
            :key="character.name" :id="`character-${character_id}`"
            :title="`${character.appearances} Quote${character.appearances > 1 ? 's' : ''}`"
            :to="{ name: 'Character', params: { character: character_id } }"
        >
            {{ character.name }}
            <b-badge class="ml-1">{{ character.appearances }}</b-badge>
        </b-button>
    </div>
</template>

<script>
export default {
    props: {
        characters: {
            type: Object,
            required: true
        }
    }
};
</script>
