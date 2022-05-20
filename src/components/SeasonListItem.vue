<template>
    <b-list-group-item
        v-if="dataAvailable"
        :id="`s-${seasonNumber}-ep-${episodeNumber}`"
        :to="{name: 'Episode', params: { season: seasonNumber, episode: episodeNumber }, }"
        class="no-link episode-item" @mouseover="hoverOn"
        @mouseleave="hoverOff"
    >
        Episode {{ episodeNumber }} - "{{ title }}"
    </b-list-group-item>
    <b-list-group-item v-else>
        <Skeleton style="width: 90%" />
    </b-list-group-item>
</template>

<script>
import {types} from "@/mutation_types";
import Skeleton from "@/components/Skeleton";

export default {
    name: "SeasonListItem",
    components: {
        Skeleton
    },
    props: {
        episodeNumber: {type: Number, default: null, required: false},
        seasonNumber: {type: Number, default: null, required: false},
        title: {type: String, default: null, required: false}
    },
    data() {
        return {
            timeoutID: null
        }
    },
    computed: {
        dataAvailable() {
            return this.episodeNumber !== null &&
                this.seasonNumber !== null &&
                this.title !== null;
        }
    },
    methods: {
        hoverFetch() {
            this.$store.dispatch(types.FETCH_EPISODE, {season: this.seasonNumber, episode: this.episodeNumber})
        },
        hoverOn() {
            this.timeoutID = setTimeout(this.hoverFetch, 800);
        },
        hoverOff() {
            if (this.timeoutID !== null) {
                clearTimeout(this.timeoutID)
                this.timeoutID = null;
            }
        }
    }
}
</script>

<style scoped>

</style>
