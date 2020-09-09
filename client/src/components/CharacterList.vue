<template>
    <div class="pt-2" v-if="characters" :fluid="true">
        <b-button
            squared
            class="mx-2 my-1 character-button"
            size="sm"
            v-for="character in characters"
            :key="character.name"
            :id="`character-${character.id}`"
            :title="`${character.appearances} Quote${
        character.appearances > 1 ? 's' : ''
      }`"
            :to="{ name: 'Character', params: { character: character.id } }"
        >
            {{ character.name }}
            <b-badge class="ml-1">{{ character.appearances }}</b-badge>
        </b-button>
    </div>
</template>

<style lang="scss">
.btn {
    box-shadow: none;

    &:focus {
        box-shadow: none;
    }
}

.character-button {
    color: $grey-10;
    background-color: $grey-4;
    border-color: $grey-3;

    .badge {
        color: lighten($grey-11, 8%);
    }
}

.character-button {
    &:focus {
        background-color: $grey-6 !important;
        border-color: $grey-4 !important;

        &:active {
            box-shadow: none !important;
        }
    }

    &:hover {
        background-color: $grey-4 !important;
        border-color: $grey-3 !important;
    }

    &:active {
        background-color: $grey-3 !important;
        border-color: $grey-3 !important;
    }
}

.character-button > .badge {
    background-color: $grey-7;
}

/*.btn-dark {*/
/*    &:not(:disabled), &:not {*/
/*        */
/*    }*/
/*}*/

/*.btn-dark:not(:disabled):not(.disabled):active, .btn-dark:not(:disabled):not(.disabled).active, {*/
/*    color: #ffffff;*/
/*    background-color: #1d2124;*/
/*    border-color: #171a1d;*/
/*}*/
</style>

<script>
export default {
    name: "CharacterList",
    props: ["characters"],
};
</script>
