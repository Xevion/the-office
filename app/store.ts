import { defineStore } from 'pinia';

// export interface Character {
//   name: string;
//   appearances: number;
//   summary: string;
// }

// export interface Season {
//   season_id: number;
//   episodes: Episode[];
// }

// export type LoadedEpisode = {
//   loaded: true;
//   title: string;
//   description: string;
//   scenes: [Scene, ...Scene[]];
//   characters: Record<string, Character>;
// };

// export type PreloadedEpisode = {
//   loaded: false;
//   title: string;
//   description: string;
//   scenes: [];
//   characters: Record<string, Character>;
// };

// export type UnloadedEpisode = {
//   loaded: false;
//   scenes: [];
// };

// export type Episode = {
//   seasonNumber: number;
//   episodeNumber: number;
// } & (LoadedEpisode | PreloadedEpisode | UnloadedEpisode);

// export interface Scene {
//   scene_id: number;
//   scene_number: number;
//   scene_name: string;
// }

// export interface Preloaded {
//   episodes: boolean;
//   characters: boolean;
// }

// // Generate 'base' representing episode data
// const episodeCount = [6, 22, 23, 14, 26, 24, 24, 24, 23];
// const baseData: Season[] = Array.from({ length: 9 }, (_, season) => {
//   // Array of null values representing each episode
//   const episodeData: Episode[] = Array.from({ length: episodeCount[season] }, (_, episode) => {
//     return { seasonNumber: season + 1, episodeNumber: episode + 1, loaded: false, scenes: [] };
//   });
//   return { season_id: season + 1, episodes: episodeData };
// });

// const useStore = defineStore('main', {
//   state: () => {
//     return {
//       seasonCount: 9 as number,
//       episodeCount: episodeCount as number[],
//       quoteData: baseData as Season[],
//       preloaded: { episodes: false, characters: false } as Preloaded,
//       characters_loaded: false as boolean,
//       characters: {} as Record<string, Character>,
//     };
//   },
//   actions: {
//     // Fully set episode data
//     setEpisode(payload: { season: number; episode: number; episodeData: Episode }) {
//       this.quoteData[payload.season - 1].episodes[payload.episode - 1] = payload.episodeData;
//     },
//     // Merge many episodes data simultaneously
//     mergeEpisodes(payload: Episode[][]) {
//       for (const season of payload) {
//         for (const episode of season) {
//           if (episode === null) {
//             console.log(`Missing Episode`);
//             continue;
//           }

//           const s = episode.seasonNumber! - 1;
//           const e = episode.episodeNumber! - 1;
//           this.quoteData[s].episodes[e] = Object.assign(this.quoteData[s].episodes[e], episode);

//           // If scenes are included for some reason, mark as a fully loaded episode
//           if (episode.scenes !== undefined) this.quoteData[s].episodes[e].loaded = true;
//         }
//       }
//     },
//     // 'Merge' episode data, overwriting existing attributes as needed
//     mergeEpisode(payload: { season: number; episode: number; episodeData: Episode }) {
//       const s = payload.season - 1;
//       const e = payload.episode - 1;
//       this.quoteData[s].episodes[e] = Object.assign(
//         this.quoteData[s].episodes[e],
//         payload.episodeData,
//       );

//       // If the episodeData has scenes, it means that this is a full episode data merge - mark it as 'loaded'
//       if (payload.episodeData.scenes !== undefined) this.quoteData[s].episodes[e].loaded = true;
//     },
//     setPreloaded(payload: { type: keyof Preloaded; status: boolean }) {
//       this.preloaded[payload.type] = payload.status;
//     },
//     setCharacter(payload: { id: string; characterData: Character }) {
//       this.characters[payload.id] = payload.characterData;
//     },
//     mergeCharacters(payload: { characters: Record<string, Character> }) {
//       // Iterate and store.
//       for (const [charId, charData] of Object.entries(payload.characters)) {
//         this.characters[charId] = charData;
//       }
//     },
//     // Perform async API call to fetch specific Episode data
//     fetchEpisode(payload: { season: number; episode: number }): Promise<void> {
//       return new Promise((resolve, reject) => {
//         // Don't re-fetch API data if it's already loaded
//         if (this.isFetched(payload.season, payload.episode)) {
//           resolve();
//           return;
//         }

//         const path = `/json/${payload.season.toString().padStart(2, '0')}/${payload.episode.toString().padStart(2, '0')}.json`;
//         // axios
//         //   .get(path)
//         //   .then((res) => {
//         //     // Push episode data
//         //     this.mergeEpisode({
//         //       season: payload.season,
//         //       episode: payload.episode,
//         //       episodeData: res.data,
//         //     });
//         //     resolve();
//         //   })
//         //   .catch((error) => {
//         //     console.error(error);
//         //     reject(error);
//         //   });
//       });
//     },
//     preloadEpisodes(): void {
//       const path = `/json/episodes.json`;

//       // axios
//       //   .get(path)
//       //   .then((res) => {
//       //     this.mergeEpisodes(res.data as Episode[][]);
//       //     this.setPreloaded({ type: 'episodes', status: true });
//       //   })
//       //   .catch((error) => {
//       //     console.error(error);
//       //   });
//     },
//     async preloadCharacters(): Promise<void> {
//       if (this.checkPreloaded('characters')) return;

//       const path = `/json/characters.json`;
//       const res = null;
//       // try {
//       //   res = await axios.get(path);
//       // } catch (error) {
//       //   console.error(error);
//       //   throw error;
//       // }

//       // this.mergeCharacters({ characters: res.data });
//       this.setPreloaded({ type: 'characters', status: true });
//     },
//   },
//   getters: {
//     checkPreloaded:
//       (state) =>
//       (identifier: keyof Preloaded): boolean => {
//         // Check whether a certain resource identifier is preloaded
//         return state.preloaded[identifier] === true;
//       },
//     // Check whether a episode has been fetched yet
//     isFetched:
//       (state) =>
//       (season: number, episode: number): boolean => {
//         const ep = state.quoteData[season - 1]?.episodes[episode - 1];
//         return ep.loaded;
//       },
//     // Get the number of episodes present for a given season
//     getEpisodeCount:
//       (state) =>
//       (season: number): number => {
//         return state.episodeCount[season - 1];
//       },
//     // return Episode data if present
//     getEpisode:
//       (state) =>
//       (season: number, episode: number): Episode | null => {
//         return state.quoteData[season - 1]?.episodes[episode - 1] ?? null;
//       },
//     // return true if a specific episode is valid
//     isValidEpisode:
//       (state) =>
//       (season: number, episode: number = 1): boolean => {
//         return (
//           season >= 1 && season <= 9 && episode >= 1 && episode <= state.episodeCount[season - 1]
//         );
//       },
//     getCharacter:
//       (state) =>
//       (character_id: string): Character | undefined => {
//         return state.characters[character_id];
//       },
//     getSortedCharacters: (state) => (): string[] => {
//       const keys = Object.keys(state.characters);
//       console.log(keys);
//       keys.sort((a, b) => {
//         const a_count = state.characters[a].appearances;
//         const b_count = state.characters[b].appearances;
//         if (a_count < b_count) return 1;
//         else return -1;
//       });
//       return keys;
//     },
//   },
// });

const useStore = defineStore('main', {});

export default useStore;
