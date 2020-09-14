<template>
    <div>
        <b-breadcrumb v-if="ready" :items="breadcrumbs"></b-breadcrumb>
        <b-card v-else class="breadcrumb-skeleton mb-3">
            <Skeleton style="width: 40%;"></Skeleton>
        </b-card>
        <b-card>
            <h4 v-if="character">{{ this.$route.params.character }}</h4>
            <Skeleton v-else style="max-width: 30%"></Skeleton>
        </b-card>
    </div>
</template>

<style lang="scss" scoped>
.breadcrumb-skeleton {
    background-color: $grey-3;
    height: 48px;

    & > .card-body {
        padding: 0 0 0 1em;
        display: flex;
        align-items: center;
    }
}
</style>

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
