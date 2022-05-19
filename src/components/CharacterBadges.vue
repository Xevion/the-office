<template>
    <div v-if="characters" class="pt-2" :fluid="true">
        <b-button
            v-for="(character, character_id) in characters" :id="`character-${character_id}`"
            :key="character.name" squared
            class="mx-2 my-1 character-button" size="sm"
            :title="`${character.appearances} Quote${character.appearances > 1 ? 's' : ''}`"
            :to="{ name: 'Character', params: { character: character_id } }"
        >
            {{ character.name }}
            <b-badge class="ml-1">
                {{ character.appearances }}
            </b-badge>
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
