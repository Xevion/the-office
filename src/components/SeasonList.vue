<template>
    <div class="accordion" role="tablist">
        <b-card v-for="season in seasons" :key="season.season_id" class="season-item">
            <b-card-header v-b-toggle="'accordion-' + season.season_id" header-tag="header" role="tab">
                <a v-if="isPreloaded" class="no-link align-items-center justify-content-between d-flex">
                    <h5 class="mb-0 pu-0 mu-0 season-title">
                        Season {{ season.season_id }}
                    </h5>
                    <b-icon class="" icon="chevron-down" />
                </a>
                <Skeleton v-else />
            </b-card-header>
            <b-collapse :id="'accordion-' + season.season_id" accordion="accordion-season-list">
                <b-card-body class="h-100 px-0">
                    <b-list-group>
                        <template v-for="(episode, index) in seasons[season.season_id - 1].episodes">
                            <template v-if="isPreloaded">
                                <b-list-group-item
                                    :id="`s-${season.season_id}-ep-${episode.episode_id}`" :key="`rl-${episode.episode_id}`"
                                    class="no-link episode-item"
                                    :to="{name: 'Episode', params: { season: season.season_id, episode: episode.episode_id }, }"
                                >
                                    Episode {{ episode.episode_id }} - "{{ episode.title }}"
                                </b-list-group-item>
                                <b-popover
                                    :key="`bpop-${episode.episode_id}`" triggers="hover"
                                    placement="right" delay="25"
                                    :target="`s-${season.season_id}-ep-${episode.episode_id}`"
                                >
                                    <template v-slot:title>
                                        {{ episode.title }}
                                    </template>
                                    {{ episode.description }}
                                </b-popover>
                            </template>
                            <b-list-group-item v-else :key="index" class="no-link episode-item">
                                <Skeleton />
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
    created() {
        this.$store.dispatch(types.PRELOAD)
    },
    methods: {},
};
</script>
