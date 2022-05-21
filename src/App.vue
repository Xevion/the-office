<template>
    <div id="app">
        <div class="wrapper">
            <b-navbar>
                <b-navbar-brand>
                    <router-link :to="{ name: 'Home' }" class="no-link">
                        The Office
                    </router-link>
                    <b-badge v-if="showBreakpointMarker" style="font-size: 0.80rem;" class="mx-2" variant="dark">
                        <span id="marker-xs" class="d-sm-none">XS</span>
                        <span id="marker-sm" class="d-none d-sm-block d-md-none">SM</span>
                        <span id="marker-md" class="d-none d-md-block d-lg-none">MD</span>
                        <span id="marker-lg" class="d-none d-lg-block d-xl-none">LG</span>
                        <span id="marker-xl" class="d-none d-xl-block">XL</span>
                    </b-badge>
                </b-navbar-brand>
                <b-collapse id="nav-collapse" is-nav>
                    <b-navbar-nav>
                        <b-nav-item href="#">
                            <router-link :to="{ name: 'Home' }" class="no-link">
                                Home
                            </router-link>
                        </b-nav-item>
                        <b-nav-item href="#">
                            <router-link :to="{ name: 'Home' }" class="no-link">
                                About
                            </router-link>
                        </b-nav-item>
                        <b-nav-item href="#">
                            <router-link :to="{ name: 'Characters' }" class="no-link">
                                Characters
                            </router-link>
                        </b-nav-item>
                    </b-navbar-nav>
                </b-collapse>
            </b-navbar>
            <ais-instant-search
                index-name="prod_THEOFFICEQUOTES" :search-client="searchClient"
                :insights-client="insightsClient"
            >
                <b-container :fluid="true" class="py-2 px-lg-5 px-md-4">
                    <b-row class="my-3 pl-1" cols="12">
                        <b-col lg="3" xl="2" md="12">
                            <ais-search-box ref="searchbox" placeholder="Search here…" @keydown.native="showResults" />
                            <!--<Skeleton
                                secondary-color="#3e3e3e"
                                border-radius="1px"
                                primary-color="#4A4A4A"
                                :inner-style="{ 'min-height': '35.6px' }"
                            />-->
                        </b-col>
                    </b-row>
                    <b-row align-h="start" cols="12">
                        <b-col lg="3" xl="2" md="12">
                            <SeasonList />
                        </b-col>
                        <b-col lg="8" xl="7" md="12" class="pt-md-2 pt-lg-0">
                            <router-view />
                        </b-col>
                    </b-row>
                </b-container>
                <ais-configure :analytics="true" />
            </ais-instant-search>
            <Footer :build-moment="buildMoment" />
        </div>
    </div>
</template>

<style lang="scss">
html, body, #app {
    min-height: 100vh;
    height: 100%;
}

#app {
    height: 100%;
    min-height: 100vh;

    .wrapper {
        min-height: 100%;
        position: relative;
        padding-bottom: 150px;
    }
}

.ais-InstantSearch {
    height: 100%;
}

.ais-SearchBox-form {
    border: none;
}

.ais-SearchBox-input {
    color: $grey-8;
    background-color: $grey-6;
    border-color: transparent;
    border-radius: 1px;
}

.ais-SearchBox-submitIcon,
.ais-SearchBox-resetIcon {
    > path {
        fill: $grey-9;
    }
}

.ais-SearchBox-input::placeholder {
    color: white;
}

#marker-xs {
    color: #ff0000;
}

#marker-sm {
    color: #f37506;
}

#marker-md {
    color: #0090ff;
}

#marker-lg {
    color: #05ff80;
}

#marker-xl {
    color: #82f500;
}
</style>

<script>
import algoliasearch from "algoliasearch/lite";
import SeasonList from "./components/SeasonList.vue";
import "instantsearch.css/themes/algolia-min.css";
import Footer from "./components/Footer.vue"
import moment from "moment";

export default {
    name: "App",
    components: {
        SeasonList,
        Footer
    },
    data() {
        return {
            searchClient: algoliasearch(
                process.env.VUE_APP_ALGOLIA_APP_ID,
                process.env.VUE_APP_ALGOLIA_API_KEY
            ),
            insightsClient: window.aa,
        };
    },
    computed: {
        showBreakpointMarker() {
            return process.env.NODE_ENV === 'development';
        },
        buildMoment() {
            return moment(document.documentElement.dataset.buildTimestampUtc)
        }
    },
    methods: {
        showResults() {
            if (this.$refs.searchbox.currentRefinement !== "" && this.$route.path !== "/search_results")
                this.$router.push({name: "SearchResults"});
        },
    }
};
</script>
