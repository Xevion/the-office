<template>
    <div class="accordion" role="tablist">
        <b-card class="season-item" v-for="season in seasons" :key="season.season_id">
            <b-card-header header-tag="header" role="tab" v-b-toggle="'accordion-' + season.season_id">
                <a class="no-link align-items-center justify-content-between d-flex" v-if="isPreloaded">
                    <h5 class="mb-0 pu-0 mu-0 season-title">
                        Season {{ season.season_id }}
                    </h5>
                    <b-icon class="" icon="chevron-down"></b-icon>
                </a>
                <Skeleton v-else></Skeleton>
            </b-card-header>
            <b-collapse :id="'accordion-' + season.season_id" accordion="accordion-season-list">
                <b-card-body class="h-100 px-0">
                    <b-list-group>
                        <template v-for="(episode, index) in seasons[season.season_id - 1].episodes">
                            <template v-if="isPreloaded">
                                <b-list-group-item class="no-link episode-item" :key="`rl-${episode.episode_id}`"
                                                   :to="{name: 'Episode', params: { season: season.season_id, episode: episode.episode_id }, }"
                                                   :id="`s-${season.season_id}-ep-${episode.episode_id}`">
                                    Episode {{ episode.episode_id }} - "{{ episode.title }}"
                                </b-list-group-item>
                                <b-popover :key="`bpop-${episode.episode_id}`" triggers="hover"
                                            placement="right" delay="25" :target="`s-${season.season_id}-ep-${episode.episode_id}`">
                                    <template v-slot:title>
                                        {{ episode.title }}
                                    </template>
                                    {{ episode.description }}
                                </b-popover>
                            </template>
                            <b-list-group-item v-else class="no-link episode-item" :key="index">
                                <Skeleton></Skeleton>
                            </b-list-group-item>
                        </template>
                    </b-list-group>
                </b-card-body>
            </b-collapse>
        </b-card>
    </div>
</template>

<script>
import Skeleton from './Skeleton.vue';
import {types} from "@/mutation_types";

export default {
    name: "SeasonList",
    components: {
        Skeleton
    },
    computed: {
        seasons() {
            return this.$store.state.quoteData;
        },
        // if SeasonList episode data (titles/descriptions) is loaded and ready
        isPreloaded() {
            return this.$store.state.preloaded;
        }
    },
    methods: {},
    created() {
        this.$store.dispatch(types.PRELOAD)
    },
};
</script>
