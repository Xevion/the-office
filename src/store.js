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
        preloaded: {episodes: false, characters: false},
        characters_loaded: false,
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
                for (const episode of season) {
                    if (episode === null) {
                        console.log(`Missing Episode`)
                        continue;
                    }

                    const s = episode.seasonNumber - 1;
                    const e = episode.episodeNumber - 1;
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
        [types.SET_PRELOADED](state, payload) {
            state.preloaded[payload.type] = payload.status;
        },
        [types.SET_CHARACTER](state, payload) {
            state.characters[payload.id] = payload.characterData
        },
        [types.MERGE_CHARACTERS](state, payload) {
            // Iterate and store.
            for (const [charId, charData] of Object.entries(payload.characters)) {
                state.characters[charId] = charData;
            }
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

                const path = `/json/${payload.season.toString().padStart(2, "0")}/${payload.episode.toString().padStart(2, "0")}.json`;
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
            const path = `/json/episodes.json`;

            axios.get(path)
                .then((res) => {
                    commit(types.MERGE_EPISODES, res.data)
                    commit(types.SET_PRELOADED, {type: 'episodes', status: true});
                })
                .catch((error) => {
                    // eslint-disable-next-line no-console
                    console.error(error);
                })
        },
        async [types.FETCH_CHARACTERS]({commit}) {
            const path = `/json/characters.json`;
            let res = null;
            try {
                res = await axios.get(path)
            } catch (error) {
                console.error(error);
                throw error
            }

            commit(types.MERGE_CHARACTERS, {characters: res.data})
            commit(types.SET_PRELOADED, {type: 'characters', status: 'true'})
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
        },
        getSortedCharacters: (state) => () => {
            let keys =  Object.keys(state.characters);
            console.log(keys)
            keys.sort((a, b) => {
                const a_count = state.characters[a].appearances;
                const b_count = state.characters[b].appearances
                if (a_count < b_count) return 1;
                else return -1;
            })
            return keys;
        }
    }
});
