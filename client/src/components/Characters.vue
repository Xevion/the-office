<template>
    <b-card v-if="ready">
        <b-list-group>
            <b-list-group-item v-for="(character, character_id) in characters" :key="character_id">
                <b-row align-v="start" align-content="start">
                    <b-col cols="5" md="4" lg="4" xl="3">
                        <b-img-lazy fluid-grow class="px-2" src="https://via.placeholder.com/250"></b-img-lazy>
                    </b-col>
                    <b-col>
                        <h4>
                            {{ character.name || character_id }}
                        </h4>
                        <p class="pl-3">{{ character.summary }}</p>
                    </b-col>
                </b-row>
            </b-list-group-item>
        </b-list-group>
    </b-card>
</template>
<style scoped>
</style>

<script>
import {types} from "@/mutation_types";

export default {
    created() {
        this.$store.dispatch(types.PRELOAD_CHARACTER)
            .then(() => {
                // recompute computed properties since Vuex won't do it
                this.$forceUpdate();
            });
    },
    computed: {
        ready() {
            return this.$store.state.preloaded;
        },
        characters() {
            return this.$store.state.characters;
        }
    }
}
</script>

