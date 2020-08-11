<template>
    <div class="accordion" role="tablist">
        <b-card class="season-item" v-for="season in seasons" :key="season.season_id">
            <b-card-header header-tag="header" role="tab">
                <a class="no-link align-items-center justify-content-between d-flex"
                   v-b-toggle="'accordion-' + season.season_id">
                    <h5 class="mb-0 pu-0 mu-0 season-title">
                        Season {{ season.season_id }}
                    </h5>
                    <b-icon class="" icon="chevron-down"></b-icon>
                </a>
            </b-card-header>
            <b-collapse :id="'accordion-' + season.season_id" accordion="accordion-season-list">
                <b-card-body class="h-100 px-0">
                    <b-list-group>
                        <template v-for="episode in season.episodes">
                            <b-list-group-item class="episode-item"
                                               :id="`s-${season.season_id}-ep-${episode.episode_id}`"
                                               :key="`rl-${episode.episode_id}`">
                                <router-link class="no-link"
                                             :to="`/${season.season_id}/${episode.episode_id}`">
                                    Episode {{ episode.episode_id }} - "{{ episode.title }}"
                                </router-link>
                            </b-list-group-item>
                            <b-popover show :key="`bpop-${episode.episode_id}`" variant="secondary" delay="25"
                                       :target="`s-${season.season_id}-ep-${episode.episode_id}`"
                                       triggers="hover" placement="right">
                                <template v-slot:title>{{ episode.title }}</template>
                                {{ episode.description }}
                            </b-popover>
                        </template>
                    </b-list-group>
                </b-card-body>
            </b-collapse>
        </b-card>
    </div>
</template>

<style lang="scss">
    @import "../assets/scss/_variables";

    // Make all season cards 'clickable'
    .season-item > .card-body > .card-header {
        cursor: pointer;
    }

    // Make all chevron icons rotate 180 when clicked
    .bi-chevron-down {
        -moz-transition: all 0.25s ease-in-out;
        -webkit-transition: all 0.25s ease-in-out;
        transition: all 0.25s ease-in-out;
    }

    .not-collapsed > .bi-chevron-down {
        transform: rotate(180deg);
        -ms-transform: rotate(180deg);
        -moz-transform: rotate(180deg);
        -webkit-transform: rotate(180deg);
    }

    // White popovers use white background on top left/right corners, this disables it.
    .b-popover {
        background: transparent;
    }

    // Dark theme popover
    .popover-header {
        background-color: darken($grey-2, 2.1%);
        border-color: $grey-1;
        color: $grey-11;
    }

    // Dark theme popover, arrow-right fix
    .bs-popover-right > .arrow::after, .bs-popover-auto[x-placement^="right"] > .arrow::after {
        border-right-color: darken($grey-3, 2%);
    }

    .season-item .list-group-item:first-child {
        border-radius: 0;
    }

    // Dark theme popover body
    .popover-body {
        color: $grey-10;
        background-color: darken($grey-3, 2%);
    }

    .season-title { color: $grey-8; cursor: pointer; }

    // Season Card Background Color
    .season-item {
        .card-body {
            padding: 0;
        }
        .card-header {
            background-color: darken($grey-2, 1.5%);
            color: $grey-9;
            border-bottom: 1px solid $grey-0;
            font-family: 'Montserrat', sans-serif;
        }
    }

    .episode-item {
        border-color: $grey-2;
        background-color: darken($grey-3, 2%);
        color: $grey-8;
        border-left-width: 0;
        border-right-width: 0;

        &:hover { background-color: darken($grey-3, 1%); }
    }

    .no-link {
        color: inherit;
        text-decoration: none;

        &:hover {
            color: inherit;
            text-decoration: none;
        }
    }
</style>

<script>
import axios from 'axios';

export default {
  name: 'SeasonList',
  data() {
    return {
      seasons: [],
    };
  },
  methods: {
    getSeasons() {
      const path = `${process.env.VUE_APP_BASE_APP_URL}/api/episodes/`;
      axios.get(path)
        .then((res) => {
          this.seasons = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.error(error);
        });
    },
  },
  created() {
    this.getSeasons();
  },
};
</script>
