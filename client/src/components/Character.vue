<template>
    <div>
        <b-breadcrumb :items="breadcrumbs"></b-breadcrumb>
        <b-card>
            <h4 v-if="character">{{ this.$route.params.character }}</h4>
            <Skeleton v-else style="max-width: 30%"></Skeleton>
        </b-card>
    </div>
</template>

<script>
import Skeleton from './Skeleton.vue';

export default {
    data() {
        return {
            character: null,
        };
    },
    components: {
        Skeleton,
    },
    computed: {
        breadcrumbs() {
            return [
                {
                    text: 'Home',
                    to: {name: 'Home'},
                },
                {
                    text: 'Characters',
                    to: {name: 'Home'},
                },
                {
                    text:
                        this.character !== null
                            ? this.character.name
                            : this.$route.params.character,
                    active: true,
                },
            ];
        },
    },
    methods: {},
};
</script>
