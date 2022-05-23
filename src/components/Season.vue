<template>
    <div>
        <b-breadcrumb :items="breadcrumbs" />
        <b-card v-if="ready">
            <b-list-group>
                <b-list-group-item v-for="episode in season.episodes" :key="episode.episode_id">
                    <b-row align-v="start" align-content="start">
                        <b-col cols="5" md="4" lg="4" xl="3">
                            <b-img-lazy
                                fluid-grow class="px-2"
                                width="200" height="200"
                                blank-width="200" blank-height="200"
                                :src="getUrl(episode.episodeNumber, episode.seasonNumber)"
                                :blank-src="getUrl(episode.episodeNumber, episode.seasonNumber, true)"
                            />
                        </b-col>
                        <b-col>
                            <h4>
                                {{ episode.title }}
                                <router-link
                                    class="no-link"
                                    :to="getEpisodeRoute(season.season_id, episode.episode_id)"
                                >
                                    <b-icon class="h6" icon="caret-right-fill" />
                                </router-link>
                            </h4>
                            <p class="pl-3">
                                {{ episode.description }}
                            </p>
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
export default {
    computed: {
        ready() {
            return this.$store.getters.checkPreloaded('episodes');
        },
        breadcrumbs() {
            return [
                {
                    text: 'Home',
                    to: {name: 'Home'}
                },
                {
                    text: `Season ${this.$route.params.season}`,
                    active: true
                }
            ]
        },
        season() {
            return this.$store.state.quoteData[this.$route.params.season - 1];
        }
    },
    methods: {
        getEpisodeRoute(s, e) {
            return {name: 'Episode', params: {season: s, episode: e}}
        },
        getUrl(episode, season, thumbnail = false) {
            episode = episode.toString().padStart(2, "0")
            season = season.toString().padStart(2, "0")
            const filename = thumbnail ? 'thumbnail.jpeg' : 'full.jpeg'

            return `/img/${season}/${episode}/${filename}`
        }
    }
}
</script>
