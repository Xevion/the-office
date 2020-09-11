<template>
    <div>
        <b-breadcrumb :items="breadcrumbs"></b-breadcrumb>
        <b-card class="mb-4">
            <template v-if="episode !== null">
                <h3>"{{ episode.title }}"</h3>
                <span v-if="episode">
                {{ episode.description }}
            </span>
                <CharacterList
                    v-if="episode && episode.characters"
                    :characters="episode.characters"
                ></CharacterList>
            </template>
            <template v-else>
                <Skeleton style="width: 30%;"></Skeleton>
                <Skeleton style="width: 70%; height: 60%;"></Skeleton>
                <Skeleton style="width: 45%; height: 60%;"></Skeleton>
                <Skeleton style="width: 69%; height: 40%;"></Skeleton>
            </template>
        </b-card>
        <div v-if="episode != null">
            <b-card
                v-for="(scene, sceneIndex) in episode.scenes"
                :key="`scene-${sceneIndex}`"
                class="mb-1"
                body-class="p-0"
            >
                <b-card-text class="my-2">
                    <QuoteList
                        :quotes="scene.quotes"
                        :sceneIndex="sceneIndex"
                    ></QuoteList>
                    <span
                        v-if="scene.deleted"
                        class="mt-n2 mb-4 text-muted deleted-scene pl-2"
                        :footer="`Deleted Scene ${scene.deleted}`"
                    >
            Deleted Scene {{ scene.deleted }}
          </span>
                </b-card-text>
            </b-card>
        </div>
    </div>
</template>

<style lang="scss">
.card-title {
    font-family: "Montserrat", sans-serif;
    font-weight: 600;
}

.deleted-scene {
    font-size: 0.75em;
    line-height: 12px;
}
</style>

<script>
import axios from "axios";
import QuoteList from "./QuoteList.vue";
import CharacterList from "./CharacterList.vue";
import Skeleton from './Skeleton.vue';

export default {
    name: "Episode",
    components: {
        QuoteList,
        CharacterList,
        Skeleton,
    },
    data() {
        return {
            episode: null,
        };
    },
    methods: {
        getEpisode() {
            const path = `${process.env.VUE_APP_API_URL}/api/episode/\
${this.$route.params.season}/${this.$route.params.episode}/`;
            axios
                .get(path)
                .then((res) => {
                    this.episode = res.data;
                    // Scroll
                    if (this.$route.hash) {
                        this.$nextTick(() => {
                            const section = document.getElementById(this.$route.hash.substring(1));
                            this.$scrollTo(section, 500, {easing: "ease-in"});
                        });
                    }
                })
                .catch((error) => {
                    // eslint-disable-next-line no-console
                    console.error(error);
                });
        },
    },
    created() {
        this.getEpisode();
    },
    watch: {
        $route() {
            this.episode = null;
            this.$nextTick(() => {
                this.getEpisode();
            })
        },
    },
    computed: {
        breadcrumbs() {
            return [
                {
                    text: 'Home',
                    to: {
                        name: 'Home'
                    }
                },
                {
                    text: `Season ${this.$route.params.season}`,
                    to: {
                        name: 'Season',
                        season: this.$route.params.season
                    }
                },
                {
                    text: `Episode ${this.$route.params.episode}`,
                    to: {
                        name: 'Episode',
                        season: this.$route.params.season,
                        episode: this.$route.params.episode
                    },
                    active: true
                }
            ]
        }
    }
};
</script>
