<template>
    <b-card class="mb-1" body-class="p-0 expandable-result" footer-class="my-1" v-on:click="toggleExpansion()">
        <b-card-text class="mu-2 py-1 mb-1">
            <table v-if="expanded" class="quote-list px-3 py-1 w-100">
                <tr v-for="(quote, index) in above" :key="`quote-a-${index}`">
                    <td class="quote-speaker my-3 pl-3">{{ quote.speaker }}</td>
                    <td class="quote-text w-100 pr-3">{{ quote.text }}</td>
                </tr>
                <tr>
                    <td class="quote-speaker my-3 pl-3" v-html="item._highlightResult.speaker.value"></td>
                    <td class="quote-text w-100 pr-3" v-html="item._highlightResult.text.value"></td>
                </tr>
                <tr v-for="(quote, index) in below" :key="`quote-b-${index}`">
                    <td class="quote-speaker my-3 pl-3">{{ quote.speaker }}</td>
                    <td class="quote-text w-100 pr-3">{{ quote.text }}</td>
                </tr>
            </table>
            <table v-else class="quote-list px-3 py-1 w-100">
                <tr v-for="(quote, index) in above" :key="`quote-a-${index}`">
                <tr>
                    <td class="quote-speaker my-3 pl-3" v-html="item._highlightResult.speaker.value"></td>
                    <td class="quote-text w-100 pr-3" v-html="item._highlightResult.text.value"></td>
                </tr>
            </table>
            <router-link v-if="expanded" class="no-link search-result-link w-100 text-muted mb-2 ml-2"
                         :to="`/${item.season}/${item.episode_rel}#${item.section_rel}`">
                Season {{ item.season }} Episode {{ item.episode_rel }} Scene {{ item.section_rel }}
            </router-link>
        </b-card-text>
    </b-card>
</template>

<style lang="scss">
    .expandable-result {
        cursor: pointer;
    }

    .collapse {
        display: block;
    }

    .search-result-link {
        white-space: nowrap;
        font-size: 0.75em !important;
    }

    .quote-list > tr {
        white-space: nowrap;

        &:hover { background-color: #242424; }
    }

    .quote-text {
        white-space: normal;
    }

    .quote-speaker {
        min-width: 75px;
        padding-right: 1em;
        font-weight: 600;
        vertical-align: text-top;
        text-align: right;
        font-family: 'Montserrat', sans-serif;
    }
</style>

<script>
import axios from 'axios';

export default {
  props: ['item'],
  data() {
    return {
      expanded: false,
      hasExpanded: false,
      above: null,
      below: null,
    };
  },
  methods: {
    toggleExpansion() {
      this.expanded = !this.expanded;
      // if first time expanding, fetch quotes
      if (!this.hasExpanded && this.expanded) {
        this.hasExpanded = true;
        this.fetchQuotes();
      }
    },
    fetchQuotes() {
      const path = `http://${process.env.VUE_APP_HOST}:${process.env.VUE_APP_FLASK_PORT}/api/quote_surround?season=\
${this.item.season}&episode=${this.item.episode_rel}&scene=${this.item.section_rel}&quote=${this.item.quote_rel}`;
      axios.get(path)
        .then((res) => {
          this.above = res.data.above;
          this.below = res.data.below;
        })
        .catch((error) => {
          // eslint-disable-next-line no-console
          console.error(error);
        });
    },
  },
};
</script>
