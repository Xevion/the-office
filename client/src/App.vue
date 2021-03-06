<template>
    <div id="app">
        <b-navbar>
            <b-navbar-brand>
                <router-link :to="{ name: 'Home' }" class="no-link">The Office Quotes</router-link>
                <b-badge style="font-size: 0.80rem;" class="mx-2" v-if="showBreakpointMarker" variant="dark">
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
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
        <ais-instant-search index-name="prod_THEOFFICEQUOTES" :search-client="searchClient"
                            :insights-client="insightsClient">
            <b-container :fluid="true" class="py-2 px-lg-5 px-md-4">
                <b-row class="my-3 pl-1" cols="12">
                    <b-col lg="3" xl="2" md="12">
                        <ais-search-box @keydown.native="showResults" ref="searchbox" placeholder="Search here…"/>
                        <Skeleton secondary_color="#3e3e3e" border_radius="1px" primary_color="#4A4A4A"
                                  :inner_style="{ 'min-height': '35.6px' }"></Skeleton>
                    </b-col>
                </b-row>
                <b-row align-h="start" cols="12">
                    <b-col lg="3" xl="2" md="12">
                        <SeasonList></SeasonList>
                    </b-col>
                    <b-col lg="8" xl="7" md="12" class="pt-md-2 pt-lg-0">
                        <router-view/>
                    </b-col>
                </b-row>
            </b-container>
            <ais-configure :clickAnalytics="true"/>
        </ais-instant-search>
    </div>
</template>

<style lang="scss">
.outer-skeleton:not(:first-child) {
    display: none;
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
import Skeleton from "./components/Skeleton.vue";

export default {
    name: "App",
    components: {
        SeasonList,
        Skeleton
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
    methods: {
        showResults() {
            if (this.$refs.searchbox.currentRefinement !== "" && this.$route.path !== "/search_results")
                this.$router.push({name: "SearchResults"});
        },
    },
    computed: {
        showBreakpointMarker() {
            return process.env.NODE_ENV === 'development';
        }
    }
};
</script>
