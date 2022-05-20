<template>
    <div class="outer-footer">
        <footer class="inner-footer">
            <b-container>
                <b-row style="text-align: center">
                    <ul>
                        <li>
                            <a href="https://github.com/Xevion/the-office">GitHub</a>
                        </li>
                        <li>
                            <a :href="latestCommitUrl">Latest Commit</a>
                        </li>
                        <li>
                            <a href="https://github.com/Xevion/the-office/issues/new">Report Issues</a>
                        </li>
                        <li>
                            <a href="https://xevion.dev">Xevion.dev</a>
                        </li>
                    </ul>
                </b-row>
                <p v-if="buildTimeString !== null" class="build-time" :title="buildISOString">
                    built on {{ buildTimeString }}
                </p>
            </b-container>
        </footer>
    </div>
</template>

<script>
export default {
    name: "Footer",
    props: {
        buildMoment: {type: Object, default: null}
    },
    computed: {
        buildTimeString() {
            return this.buildMoment.format('MMM do, YYYY [at] h:mm A zz')
        },
        buildISOString() {
            return this.buildMoment.toISOString()
        },
        latestCommitUrl() {
            return `https://github.com/Xevion/the-office/commit/${process.env.VUE_APP_GIT_HASH}`
        }
    }
}
</script>

<style lang="scss" scoped>
.outer-footer {
    height: 100px;
    width:100%;
    position: absolute;
    left: 0;
    bottom: 0;
}

.inner-footer {
    margin: 0 auto;
    height: 100%;
    color: #6d6d6d;

    .build-time {
        text-align: center;
        padding-top: 0.7em;
        opacity: 0.3;
        font-size: 0.85em;
        margin-bottom: 0;
    }

    ul {
        padding: 0;
        list-style: none;
        line-height: 1.6;
        font-size: 14px;
        display: table;
        margin: 0 auto;

        li {
            &:not(:last-child)::after {
                padding: 0 0.6em;
                content: "|";
            }

            display: inline;
        }

        a {
            color: inherit;
            text-decoration: none;
            opacity: 0.6;

            &:hover {
                opacity: 0.8;
            }
        }
    }
}
</style>
