<template>
    <div class="pt-2" v-if="characters" :fluid=true>
        <b-button squared class="mx-2 my-1 character-button" size="sm"
                  v-for="character in characters" :key="character.name" :id="`character-${character.id}`"
                  :title="`${character.appearances} Quote${character.appearances > 1 ? 's' : ''}`"
        >
            {{ character.name }}
            <b-badge class="ml-1">{{ character.appearances}}</b-badge>
        </b-button>
    </div>
</template>

<style lang="scss">
    .btn {
        box-shadow: none;

        &:focus { box-shadow: none; }
    }

    .character-button {
        background-color: #292929;
        border-color: #1d1d1d;
    }

    .character-button {
        &:focus {
            background-color: #292929 !important;
            border-color: #1d1d1d !important;
            &:active { box-shadow: none !important;}
        }

        &:hover {
            background-color: #1d1d1d  !important;
            border-color: #161616 !important;
        }

        &:active {
            background-color: #1d1d1d !important;
            border-color: #161616 !important;
        }
    }

    .character-button > .badge {
        background-color: #565656;
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
  name: 'CharacterList',
  props: ['characters'],
};
</script>
