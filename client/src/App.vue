<template>
    <div id="app">
        <ais-instant-search index-name="prod_THEOFFICEQUOTES" :search-client="searchClient">
            <b-container :fluid="true" class="py-3 px-lg-5 px-md-4">
                <b-row class="my-3 pl-1">
                    <b-col lg="3" xl="2" md="12">
                        <ais-search-box @keydown.native="showResults" ref="searchbox" placeholder="Search here…"/>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col lg="3" xl="2" md="12">
                        <SeasonList></SeasonList>
                    </b-col>
                    <b-col class="pt-md-2 pt-lg-0">
                        <router-view/>
                    </b-col>
                    <b-col md="0" lg="0" xl="2"></b-col>
                </b-row>
            </b-container>
        </ais-instant-search>
    </div>
</template>

<style lang="scss">
    @import "assets/scss/_variables";
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    body { background-color: $grey-0; font-family: 'Roboto', sans-serif; }

    .ais-SearchBox-form {
        border: none;
    }

    .ais-SearchBox-input {
        color: $grey-8;
        background-color: $grey-6;
        border-color: transparent;
        border-radius: 1px;
    }

    .ais-SearchBox-submitIcon, .ais-SearchBox-resetIcon {
        > path { fill: $grey-9; }
    }

    .ais-SearchBox-input::placeholder {
        color: white;
    }

</style>

<script>
import algoliasearch from 'algoliasearch/lite';
import SeasonList from './components/SeasonList.vue';
import 'instantsearch.css/themes/algolia-min.css';

export default {
  name: 'App',
  components: {
    SeasonList,
  },
  data() {
    return {
      searchClient: algoliasearch(
        process.env.VUE_APP_ALGOLIA_APP_ID,
        process.env.VUE_APP_ALGOLIA_API_KEY,
      ),
    };
  },
  methods: {
    showResults() {
      if (this.$refs.searchbox.currentRefinement !== '' && this.$route.path !== '/search_results') {
        this.$router.push({ name: 'SearchResults' });
      }
    },
  },
};
</script>
