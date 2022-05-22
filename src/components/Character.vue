<template>
    <div>
        <b-breadcrumb v-if="ready" :items="breadcrumbs"></b-breadcrumb>
        <b-card v-else class="breadcrumb-skeleton mb-3">
            <Skeleton style="width: 40%;"></Skeleton>
        </b-card>
        <b-card>
            <h4 v-if="ready">{{ character.name }}</h4>
            <Skeleton v-else style="max-width: 30%"></Skeleton>
            <b-card-body v-if="ready">
                {{ character.summary }}
            </b-card-body>
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
import {types} from "@/mutation_types";

export default {
    name: 'Character',
    components: {
        Skeleton,
    },
    data() {
        return {
            character: null
        }
    },
    computed: {
        ready() {
            return this.character !== undefined && this.character !== null;
        },
        breadcrumbs() {
            return [
                {
                    text: 'Home',
                    to: {name: 'Home'},
                },
                {
                    text: 'Characters',
                    to: {name: 'Characters'},
                },
                {
                    text:
                        this.character !== null && this.character !== undefined
                            ? this.character.name || this.$route.params.character
                            : this.$route.params.character,
                    active: true,
                },
            ];
        },
    },
    created() {
        this.fetchCharacter();
    },
    watch: {
        $route() {
            this.$nextTick(() => {
                this.fetchCharacter();
            })
        }
    },
    created() {
        this.fetchCharacter();
    },
    methods: {
        fetchCharacter() {
            this.$store.dispatch(types.PRELOAD_CHARACTERS)
                .then(() => {
                    this.character = this.$store.getters.getCharacter(this.$route.params.character);
                })
        },
    },
};
</script>
