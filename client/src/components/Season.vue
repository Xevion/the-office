<template>
    <div>
        <b-breadcrumb :items="breadcrumbs"></b-breadcrumb>
        <b-card>
            <b-list-group>
                <b-list-group-item v-for="episode in season.episodes" :key="episode.episode_id">
                    <b-row align-v="start">
                        <b-col cols="3">
                            <b-img src="https://via.placeholder.com/150"></b-img>
                        </b-col>
                    <b-col>
                        <h4>{{ episode.title }}</h4>
                        <p class="pl-3">{{ episode.description }}</p>
                    </b-col>
                    </b-row>
                </b-list-group-item>
            </b-list-group>
        </b-card>
    </div>
</template>

<script>
export default {
    computed: {
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
            return this.$store.state.preloaded ? this.$store.state.quoteData[this.$route.params.season - 1] : null;
        }
    }
}
</script>
