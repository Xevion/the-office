<template>
    <b-container v-if="characters" :fluid=true>
        <b-row cols="12">
            <b-col sm="1" v-for="character in characters" :key="character.name">
                <b-button squared class="mx-1" variant="dark" size="sm" :id="`character-${character.id}`">
                    {{ character.name }}
                </b-button>
                <b-popover boundary-padding="2" :target="`character-${character.id}`" triggers="hover" placement="top"
                           :content="`${character.appearances} Quote${character.appearances > 1 ? 's' : ''}`">
                </b-popover>
            </b-col>
        </b-row>
    </b-container>
</template>

<style lang="scss">
    .btn {
        box-shadow: none;

        &:focus { box-shadow: none; }
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
