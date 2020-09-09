<template>
    <div>
        <b-breadcrumb :items="breadcrumbs"></b-breadcrumb>
        <b-card>
            <h4 v-if="character">{{ this.$route.params.character }}</h4>
            <Skeleton v-else style="max-width: 30%"></Skeleton>
        </b-card>
    </div>
</template>

<style lang="scss" scoped>
.card-body h4,
.breadcrumb-item.active {
    text-transform: capitalize;
}

.skeleton {
    min-height: 24px;
}
a {
    color: #1296ff;
    &:hover {
        color: #007fe0;
    }
}

.breadcrumb-item + .breadcrumb-item::before {
    color: $grey-10;
}

.breadcrumb {
    background-color: $grey-3;
    border-radius: 0;

    .breadcrumb-item {
        color: $grey-10;
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
