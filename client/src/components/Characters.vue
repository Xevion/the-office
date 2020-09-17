<template>
    <li>
        <em v-for="character in characters" :key="character.name">
            {{ character.name }}
        </em>
    </li>
</template>
<style scoped>
</style>

<script>
import {types} from "@/mutation_types";

export default {
    created() {
        console.log('preload character')
        this.$store.dispatch(types.PRELOAD_CHARACTER);
    },
    computed: {
        characters() {
            return this.$store.state.characters;
        }
    }
}
</script>

