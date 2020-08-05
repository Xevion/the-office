<template>
    <div class="accordion" role="tablist">
        <b-card v-for="season in seasons" :key="season.season_id">
            <b-card-header header-tag="header" role="tab">
                <a class="no-link" v-b-toggle="'accordion-' + season.season_id">
                    <h5 class="mb-0 pu-0 mu-0 season-title">
                        Season {{ season.season_id }}
                        <i class="fas fa-chevron-down float-right"></i>
                    </h5>
                </a>
            </b-card-header>
            <b-collapse :id="'accordion-' + season.season_id" accordion="accordion-season-list">
                <b-card-body class="h-100 px-0">
                    <b-list-group>
                        <b-list-group-item v-for="episode in season.episodes" :key="episode.episode_id">
                            <router-link class="no-link" :to="`/${season.season_id}/${episode.episode_id}`">
                                Ep. {{ episode.episode_id }} - "{{ episode.title }}"
                            </router-link>
                        </b-list-group-item>
                    </b-list-group>
                </b-card-body>
            </b-collapse>
        </b-card>
    </div>
</template>

<style lang="scss">
    .season-title { color: #888888; }

    .accordion.list-group-item {
        border-radius: 0;
        border-width: 0 0 0 0;
        border-bottom-width: 1px;
        padding-left: 30px;
        font-weight: 500;

        &:first-child { border-top-width: 1px; }

        &:last-child { border-bottom-width: 0; }

    }

    .accordion {
        .list-group-item {
            a { display: block; }

            .badge { float: right; min-width: 36px; }
        }

        .card-body { padding: 0; }
    }

    .card-header {
        background-color: #161616;
        border-bottom: 1px solid rgba(0, 0, 0, 0.88);
    }

    .card {
        background-color: inherit;
        /*border: 3px solid #0a0a0a;*/
        /*border-radius: 0;*/
        padding-bottom: 0px;
        /*&:not(:first-child) { border-top-width: 0; }*/
        /*&:not(:last-child) { border-bottom-width: 0; }*/
    }

    .list-group-item {
        border-color: rgba(24, 24, 24, 0.82);
        background-color: #111111;
        color: grey;
        border-left-width: 0;
        border-right-width: 0;
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
      const path = 'http://localhost:5000/api/episodes/';
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
