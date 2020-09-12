<template>
    <div class="pt-2" v-if="characters" :fluid="true">
        <b-button squared class="mx-2 my-1 character-button" size="sm" v-for="character in characters"
            :key="character.name" :id="`character-${character.id}`"
            :title="`${character.appearances} Quote${character.appearances > 1 ? 's' : ''}`"
            :to="{ name: 'Character', params: { character: character.id } }"
        >
            {{ character.name }}
            <b-badge class="ml-1">{{ character.appearances }}</b-badge>
        </b-button>
    </div>
</template>

<script>
export default {
    name: "CharacterList",
    props: ["characters"],
};
</script>
