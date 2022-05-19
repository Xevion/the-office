<template>
    <div class="outer-skeleton">
        <div class="skeleton" :class="[animated ? undefined : 'no-animate']" :style="[style, inner_style]" />
    </div>
</template>
<style lang="scss" scoped>
.skeleton {
    width: 100%;
    display: block;
    line-height: 1;
    background-size: 200px 100%;
    background-repeat: no-repeat;
    background-image: linear-gradient(90deg, var(--secondary-color, $grey-4), var(--primary-color, $grey-6), var(--secondary-color, $grey-4));
    background-color: var(--secondary-color, $grey-4);
    animation: 1.25s ease-in-out 0s infinite normal none running SkeletonLoading;
    border-radius: var(--border-radius, 3px);

    &.no-animate {
        animation: none;
    }
}

.outer-skeleton {
    padding: 0.2em 0;
}

@-webkit-keyframes SkeletonLoading {
    0% {
        background-position: -200px 0;
    }
    100% {
        background-position: calc(200px + 100%) 0;
    }
}

@keyframes SkeletonLoa,ding {
    0% {
        background-position: -200px 0;
    }
    100% {
        background-position: calc(200px + 100%) 0;
    }
}

span {
    font-size: 24px;
}
</style>

<script>
export default {
    props: {
        inner_style: {
            type: Object
        },
        inner_class: {
            type: String,
            default: ''
        },
        animated: {
            type: Boolean,
            default: true
        },
        border_radius: {
            type: String,
        },
        primary_color: {
            type: String,
        },
        secondary_color: {
            type: String,
        }
    },
    computed: {
        style() {
            return {
                '--primary-color': this.primary_color,
                '--secondary-color': this.secondary_color,
                '--border-radius': this.border_radius
            }
        }
    }
}
</script>
