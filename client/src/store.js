import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import {types} from "@/mutation_types";

Vue.use(Vuex);

// Generate 'base' representing episode data
const episodeCount = [6, 22, 23, 14, 26, 24, 24, 24, 23];
const baseData = Array.from({length: 9}, (x, season) => {
    // Array of null values representing each episode
    let episodeData = Array.from({length: episodeCount[season]}, () => null)
    return {season_id: season + 1, episodes: episodeData};
})

export default new Vuex.Store({
    state: {
        seasonCount: 9,
        episodeCount: episodeCount,
        quoteData: baseData,
    },
    mutations: {
        [types.SET_EPISODE](state, payload) {
            state.quoteData[payload.season - 1].episodes[payload.episode - 1] = payload.data
        }
    },
    actions: {
        // Perform async API call to fetch specific Episode data
        [types.FETCH_EPISODE]({commit}, season, episode) {
            const path = `${process.env.VUE_APP_API_URL}/api/episode/${season}/${episode}/`;

            axios.get(path)
                .then((res) => {
                    // Push episode data
                    commit(types.SET_EPISODE, { season: season, episode: episode, data: res.data})
                })
                .catch((error) => {
                    // eslint-disable-next-line no-console
                    console.error(error);
                });
        }
    },
    getters: {
        // Check whether a episode has been fetched yet
        isFetched(season, episode) {
            return this.$store.state.quoteData[season - 1].episodes[episode] !== null;
        },
        // Get the number of episodes present for a given season
        getEpisodeCount(season) {
            return this.$store.state.episodeCount[season - 1];
        },
        // return Episode data if present
        getEpisode(season, episode) {
            if (this.getters.isFetched(season, episode))
                return this.$store.state.quoteData[season]
            else
                return null
        },
        // return true if a specific episode is valid
        isValidEpisode(season, episode = 1) {
            return season >= 1 && season <= 9 && episode >= 1 && episode <= this.$store.getters.getEpisodeCount(season)
        }
    }
});
