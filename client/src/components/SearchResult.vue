<template>
    <b-card
        class="mb-1"
        body-class="p-0 expandable-result"
        footer-class="my-1"
        v-on:mouseover="hover"
        v-on:click="toggleExpansion"
        :class="[expanded ? 'expanded' : '']"
    >
        <b-card-text class="mu-2 py-1 mb-1">
            <table v-if="expanded" class="quote-list px-3 py-1 w-100">
                <tr
                    v-for="(quote, index) in above"
                    class="secondary"
                    :key="`quote-a-${index}`"
                >
                    <td class="quote-speaker my-3 pl-3">
                        <div>{{ quote.speaker }}</div>
                    </td>
                    <td class="quote-text w-100 pr-3">
                        <div>{{ quote.text }}</div>
                    </td>
                </tr>
                <tr>
                    <td
                        class="quote-speaker my-3 pl-3"
                        v-html="item._highlightResult.speaker.value"
                    ></td>
                    <td
                        class="quote-text w-100 pr-3"
                        v-html="item._highlightResult.text.value"
                    ></td>
                </tr>
                <tr
                    v-for="(quote, index) in below"
                    class="secondary"
                    :key="`quote-b-${index}`"
                >
                    <td class="quote-speaker my-3 pl-3">
                        <div>{{ quote.speaker }}</div>
                    </td>
                    <td class="quote-text w-100 pr-3">
                        <div>{{ quote.text }}</div>
                    </td>
                </tr>
            </table>
            <table v-else class="quote-list px-3 py-1 w-100">
                <tr>
                    <td
                        class="quote-speaker my-3 pl-3"
                        v-html="item._highlightResult.speaker.value"
                    ></td>
                    <td
                        class="quote-text w-100 pr-3"
                        v-html="item._highlightResult.text.value"
                    ></td>
                </tr>
            </table>
            <router-link
                v-if="expanded"
                class="no-link search-result-link w-100 text-muted mb-2 ml-2"
                :to="{
          name: 'Episode',
          params: { season: item.season, episode: item.episode_rel },
          hash: `#${item.section_rel - 1}-${item.quote_rel - 1}`,
        }"
            >
                Season {{ item.season }} Episode {{ item.episode_rel }} Scene
                {{ item.section_rel }}
            </router-link>
        </b-card-text>
    </b-card>
</template>

<style lang="scss">
@import "../assets/scss/_variables";

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

    &:hover {
        background-color: $grey-4;
    }
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
    font-family: "Montserrat", sans-serif;
}
</style>

<script>
import axios from "axios";

export default {
    props: ["item"],
    data() {
        return {
            expanded: false,
            fetching: false,
            above: null,
            below: null,
        };
    },
    computed: {
        fetched() {
            return this.above !== null || this.below !== null;
        },
    },
    methods: {
        toggleExpansion() {
            this.expanded = !this.expanded;
            // if first time expanding, fetch quotes
            if (!this.fetchQuotes()) {
                this.hasExpanded = true;
                this.fetchQuotes();
            }
        },
        hover() {
            if (!this.fetched && !this.fetching) {
                this.fetching = true;
                this.fetchQuotes();
                this.fetching = false;
            }
        },
        fetchQuotes() {
            const path = `${process.env.VUE_APP_API_URL}/api/quote_surround?season=\
${this.item.season}&episode=${this.item.episode_rel}&scene=${this.item.section_rel}&quote=${this.item.quote_rel}`;
            axios
                .get(path)
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
