import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import {types} from "@/mutation_types";

Vue.use(Vuex);

// Generate 'base' representing episode data
const episodeCount = [6, 22, 23, 14, 26, 24, 24, 24, 23];
const baseData = Array.from({length: 9}, (x, season) => {
    // Array of null values representing each episode
    const episodeData = Array.from({length: episodeCount[season]}, (x, episode) => {
        return {episode_id: episode + 1, loaded: false}
    })
    return {season_id: season + 1, episodes: episodeData};
})

export default new Vuex.Store({
    state: {
        seasonCount: 9,
        episodeCount: episodeCount,
        quoteData: baseData,
        preloaded: false,
        characters: {}
    },
    mutations: {
        // Fully set episode data
        [types.SET_EPISODE](state, payload) {
            state.quoteData[payload.season - 1].episodes[payload.episode - 1] = payload.episodeData
        },
        // Merge many episodes data simultaneously
        [types.MERGE_EPISODES](state, payload) {
            for (const season of payload) {
                for (const episode of season.episodes) {
                    const s = season.season_id - 1;
                    const e = episode.episode_id - 1;
                    state.quoteData[s].episodes[e] = Object.assign(state.quoteData[s].episodes[e], episode);

                    // If scenes are included for some reason, mark as a fully loaded episode
                    if (episode.scenes !== undefined)
                        state.quoteData[s].episodes[e].loaded = true;
                }
            }
        },
        // 'Merge' episode data, overwriting existing attributes as needed
        [types.MERGE_EPISODE](state, payload) {
            const s = payload.season - 1;
            const e = payload.episode - 1;
            state.quoteData[s].episodes[e] = Object.assign(state.quoteData[s].episodes[e], payload.episodeData);

            // If the episodeData has scenes, it means that this is a full episode data merge - mark it as 'loaded'
            if (payload.episodeData.scenes !== undefined)
                state.quoteData[s].episodes[e].loaded = true;
        },
        [types.SET_PRELOADED](state, status) {
            state.preloaded = status;
        },
        [types.SET_CHARACTER](state, payload) {
            state.characters[payload.id] = payload.characterData
        },
        [types.MERGE_CHARACTER](state, payload) {
            const id = payload.id;
            // If character has not been defined in character list yet, simply set the characterData
            if (state.characters[id] === undefined)
                state.characters[id] = payload.characterData
            // Otherwise use intended merge & overwrite effect.
            else
                state.characters[id] = Object.assign(state.characters[id], payload.characterData)
        },
    },
    actions: {
        // Perform async API call to fetch specific Episode data
        [types.FETCH_EPISODE](context, payload) {
            return new Promise((resolve, reject) => {
                // Don't re-fetch API data if it's already loaded
                if (context.getters.isFetched(payload.season, payload.episode)) {
                    resolve()
                    return
                }

                const path = `${process.env.VUE_APP_API_URL}/api/episode/${payload.season}/${payload.episode}/`;
                axios.get(path)
                    .then((res) => {
                        // Push episode data
                        context.commit(types.MERGE_EPISODE, {
                            season: payload.season,
                            episode: payload.episode,
                            episodeData: res.data
                        })
                        resolve()
                    })
                    .catch((error) => {
                        // eslint-disable-next-line no-console
                        console.error(error);
                        reject()
                    });
            })
        },
        [types.PRELOAD]({commit}) {
            const path = `${process.env.VUE_APP_API_URL}/api/episodes/`;

            axios.get(path)
                .then((res) => {
                    commit(types.MERGE_EPISODES, res.data)
                    commit(types.SET_PRELOADED, true);
                })
                .catch((error) => {
                    // eslint-disable-next-line no-console
                    console.error(error);
                })
        },
        [types.PRELOAD_CHARACTER]({commit}) {
            return new Promise((resolve, reject) => {
                const path = `${process.env.VUE_APP_API_URL}/api/characters/`;
                axios.get(path)
                    .then((res) => {
                        for (const [character_id, character_data] of Object.entries(res.data))
                            commit(types.MERGE_CHARACTER, {id: character_id, characterData: character_data})
                        resolve();
                    })
                    .catch((error) => {
                        console.error(error);
                        reject()
                    })
            })
        },
        [types.FETCH_CHARACTER]({commit}, character_id) {
            return new Promise((resolve, reject) => {
                const path = `${process.env.VUE_APP_API_URL}/api/character/${character_id}/`;
                axios.get(path)
                    .then((res) => {
                        commit(types.MERGE_CHARACTER, {id: character_id, characterData: res.data})
                        resolve();
                    })
                    .catch((error) => {
                        reject();
                        console.error(error);
                    })
            })
        }
    },
    getters: {
        // Check whether a episode has been fetched yet
        isFetched: (state) => (season, episode) => {
            const ep = state.quoteData[season - 1].episodes[episode - 1];
            return ep.loaded;
        },
        // Get the number of episodes present for a given season
        getEpisodeCount: (state) => (season) => {
            return state.episodeCount[season - 1];
        },
        // return Episode data if present
        getEpisode: (state, getters) => (season, episode) => {
            if (getters.isFetched(season, episode)) {
                return state.quoteData[season - 1].episodes[episode - 1];
            } else
                return null
        },
        // return true if a specific episode is valid
        isValidEpisode: (state, getters) => (season, episode = 1) => {
            return season >= 1 && season <= 9 && episode >= 1 && episode <= getters.getEpisodeCount(season)
        },
        getCharacter: (state) => (character_id) => {
            return state.characters[character_id];
        }
    }
});
