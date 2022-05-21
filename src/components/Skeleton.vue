<template>
    <div class="outer-skeleton">
        <div
            class="skeleton"
            :class="[animated ? undefined : 'no-animate']"
            :style="[style, innerStyle]"
        />
    </div>
</template>

<style lang="scss">
.breadcrumb-skeleton {
    height: 48px;

    & > .card-body {
        padding: 0 0 0 1em;
        display: flex;
        align-items: center;
    }
}

.outer-skeleton {
    padding: 0.35em 0.3em 0.35em 0.35em;

    .breadcrumb-skeleton > {
        display: inline-block;
    }

    .skeleton {
        width: 100%;
        height: 100%;
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
}

@-webkit-keyframes SkeletonLoading {
    0% {
        background-position: -200px 0;
    }
    100% {
        background-position: calc(200px + 100%) 0;
    }
}

@keyframes SkeletonLoading {
    0% {
        background-position: -200px 0;
    }
    100% {
        background-position: calc(200px + 100%) 0;
    }
}
</style>

<script>
export default {
    props: {
        innerStyle: {
            type: Object,
            default: null,
        },
        innerClass: {
            type: String,
            default: ''
        },
        animated: {
            type: Boolean,
            default: true
        },
        borderRadius: {
            type: String,
            default: ''
        },
        primaryColor: {
            type: String,
            default: '',
        },
        secondaryColor: {
            type: String,
            default: '',
        }
    },
    computed: {
        style() {
            return {
                '--primary-color': this.primaryColor,
                '--secondary-color': this.secondaryColor,
                '--border-radius': this.borderRadius
            }
        }
    }
}
</script>
