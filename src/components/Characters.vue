<template>
    <div>
        <template v-if="ready">
            <b-breadcrumb v-if="ready" :items="breadcrumbs" />
            <b-card>
                <b-list-group>
                    <b-list-group-item v-for="id in sorted_character_ids" :key="id">
                        <b-row align-v="start" align-content="start">
                            <b-col cols="5" md="4" lg="4" xl="3">
                                <b-img-lazy
                                    fluid-grow class="px-2"
                                    :src="faceURL(id)"
                                    :blank-src="faceURL(id, true)"
                                    blank-width="200" blank-height="200"
                                />
                            </b-col>
                            <b-col>
                                <h4>
                                    {{ characters[id].name || id }}
                                    <router-link
                                        class="no-link"
                                        :to="{ name: 'Character', params: {character: id} }"
                                    >
                                        <b-icon class="h6" icon="caret-right-fill" />
                                    </router-link>
                                </h4>
                                <p class="pl-3">
                                    {{ characters[id].summary }}
                                </p>
                            </b-col>
                        </b-row>
                    </b-list-group-item>
                </b-list-group>
            </b-card>
        </template>
        <template v-else>
            <b-card class="breadcrumb-skeleton mb-3">
                <Skeleton class="inlined" style="width: 10%;" />
                <Skeleton class="inlined" style="width: 30%;" />
            </b-card>
            <b-card>
                <b-list-group>
                    <b-list-group-item v-for="i in 6" :key="i">
                        <b-row align-v="start" align-content="start">
                            <b-col cols="5" lg="4" xl="3">
                                <ImageSkeleton style="width: 200px; height: 200px" />
                            </b-col>
                            <b-col>
                                <Skeleton style="width: 40%; height: 2.7em;" />
                                <Skeleton style="width: 60%;" />
                                <Skeleton style="width: 25%;" />
                                <Skeleton style="width: 35%;" />
                                <Skeleton style="width: 60%;" />
                            </b-col>
                        </b-row>
                    </b-list-group-item>
                </b-list-group>
            </b-card>
        </template>
    </div>
</template>

<style lang="scss" scoped>
h4 {
    .b-icon {
        font-size: 0.9rem;
        vertical-align: middle !important;
        position: relative;
        top: 3px;
        color: #007fe0;

        &:hover {
            color: darken(#007fe0, 10%);
        }
    }
}
</style>

<script>
import {types} from "@/mutation_types";
import Skeleton from "@/components/Skeleton.vue";
import ImageSkeleton from "@/components/ImageSkeleton";

export default {
    components: {
        ImageSkeleton,
        Skeleton
    },
    computed: {
        ready() {
            return this.$store.getters.checkPreloaded('characters');
        },
        sorted_character_ids() {
            return this.$store.getters.getSortedCharacters();
        },
        characters() {
            return this.$store.state.characters;
        },
        breadcrumbs() {
            return [
                {text: 'Home', to: {name: 'Home'}},
                {text: 'Characters', active: true}
            ]
        }
    },
    async mounted() {
        await this.$store.dispatch(types.PRELOAD_CHARACTERS)

        // Re-compute computed properties since Vuex won't do it
        // this.$forceUpdate();
    },
    methods: {
        faceURL(character, thumbnail = false) {
            return `/img/${character}/` + (thumbnail ? "face_thumb" : "face") + ".webp";
        }
    }
}
</script>

