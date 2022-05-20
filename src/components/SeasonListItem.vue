<template>
    <b-list-group-item
        :id="`s-${seasonNumber}-ep-${episodeNumber}`"
        :to="{name: 'Episode', params: { season: seasonNumber, episode: episodeNumber }, }"
        class="no-link episode-item"
        @mouseover="hoverOn" @mouseleave="hoverOff"
    >
        Episode {{ episodeNumber }} - "{{ title }}"
    </b-list-group-item>
</template>

<script>
import {types} from "@/mutation_types";

export default {
    name: "SeasonListItem",
    props: {
        episodeNumber: {type: Number, default: null, required: true},
        seasonNumber: {type: Number, default: null, required: true},
        title: {type: String, default: null, required: true}
    },
    data() {
        return {
            timeoutID: null
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
