<template>
    <div>
        <b-breadcrumb v-if="ready" :items="breadcrumbs"></b-breadcrumb>
        <b-card v-else class="breadcrumb-skeleton mb-3">
            <Skeleton style="width: 40%;"></Skeleton>
        </b-card>
        <b-card v-if="ready">
            <b-list-group>
                <b-list-group-item v-for="(character, character_id) in characters" :key="character_id">
                    <b-row align-v="start" align-content="start">
                        <b-col cols="5" md="4" lg="4" xl="3">
                            <b-img-lazy fluid-grow class="px-2" :src="faceURL(character_id)"
                                        :blank-src="faceURL(character_id, thumbnail = true)"
                                        blank-width="200" blank-height="200"
                            ></b-img-lazy>
                            <!--                            <b-img fluid-grow class="px-2"></b-img>-->
                        </b-col>
                        <b-col>
                            <h4>
                                {{ character.name || character_id }}
                                <router-link class="no-link"
                                             :to="{ name: 'Character', params: {character: character_id} }">
                                    <b-icon class="h6" icon="caret-right-fill"></b-icon>
                                </router-link>
                            </h4>
                            <p class="pl-3">{{ character.summary }}</p>
                        </b-col>
                    </b-row>
                </b-list-group-item>
            </b-list-group>
        </b-card>
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

export default {
    components: {
        Skeleton
    },
    methods: {
        faceURL(character, thumbnail = false) {
            return `${process.env.VUE_APP_API_URL}/static/img/${character}/` + (thumbnail ? "face_thumb.webp" : "face.webp");
        }
    },
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
        },
        breadcrumbs() {
            return [
                {text: 'Home', to: {name: 'Home'}},
                {text: 'Characters', active: true}
            ]
        }
    }
}
</script>

