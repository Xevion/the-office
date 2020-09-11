<template>
    <div class="accordion" role="tablist">
        <b-card
            class="season-item"
            v-for="season in seasons"
            :key="season.season_id"
        >
            <b-card-header
                header-tag="header"
                role="tab"
                v-b-toggle="'accordion-' + season.season_id"
            >
                <a class="no-link align-items-center justify-content-between d-flex">
                    <h5 class="mb-0 pu-0 mu-0 season-title">
                        Season {{ season.season_id }}
                    </h5>
                    <b-icon class="" icon="chevron-down"></b-icon>
                </a>
            </b-card-header>
            <b-collapse
                :id="'accordion-' + season.season_id"
                accordion="accordion-season-list"
            >
                <b-card-body class="h-100 px-0">
                    <b-list-group>
                        <template v-for="episode in season.episodes">
                            <b-list-group-item
                                class="no-link episode-item"
                                :id="`s-${season.season_id}-ep-${episode.episode_id}`"
                                :key="`rl-${episode.episode_id}`"
                                :to="{
                  name: 'Episode',
                  params: {
                    season: season.season_id,
                    episode: episode.episode_id,
                  },
                }"
                            >
                                Episode {{ episode.episode_id }} - "{{ episode.title }}"
                            </b-list-group-item>
                            <b-popover
                                show
                                :key="`bpop-${episode.episode_id}`"
                                variant="secondary"
                                delay="25"
                                :target="`s-${season.season_id}-ep-${episode.episode_id}`"
                                triggers="hover"
                                placement="right"
                            >
                                <template v-slot:title>{{ episode.title }}</template>
                                {{ episode.description }}
                            </b-popover>
                        </template>
                    </b-list-group>
                </b-card-body>
            </b-collapse>
        </b-card>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "SeasonList",
    data() {
        return {
            seasons: [],
        };
    },
    methods: {
        getSeasons() {
            const path = `${process.env.VUE_APP_API_URL}/api/episodes/`;
            axios
                .get(path)
                .then((res) => {
                    this.seasons = res.data;
                })
                .catch((error) => {
                    // eslint-disable-next-line no-console
                    console.error(error);
                });
        },
    },
    created() {
        this.getSeasons();
    },
};
</script>
