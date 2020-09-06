<template>
    <table class="quote-list px-3 w-100">
        <tr v-for="(quote, index) in quotes" :key="`quote-${index}`" :id="`${sceneIndex}-${index}`"
            :class="$route.hash !== null && $route.hash.substring(1) === `${sceneIndex}-${index}` ? 'highlight' : ''">
            <td class="quote-speaker pl-3" v-if="quote.speaker">
                <span class="my-3">
                    {{ quote.speaker }}
                </span>
            </td>
            <td class="quote-text w-100 pr-3">{{ quote.text }}</td>
            <td class="px-1 pl-2">
                <a :href="quote_link(index)" class="no-link">
                    <b-icon icon="link45deg"></b-icon>
                </a>
            </td>
        </tr>
    </table>
</template>

<style lang="scss">
@import "../assets/scss/_variables";
.quote-list > tr {
    white-space: nowrap;

    &:hover {
        background-color: $grey-4;
    }
    &.highlight {
        background-color: $grey-5 !important;
    }
}

.quote-text {
    white-space: normal;
}

.quote-speaker {
    color: darken($grey-10, 1.75%);
    min-width: 100px;
    padding-right: 1em;
    font-weight: 600;
    vertical-align: text-top;
    text-align: right;
    font-family: 'Montserrat', sans-serif;
}

table.quote-list tr td:last-child {
    height: 100%;
    a { height: 100%; }
    svg {
        font-size: 1.35em;
        opacity: 0;
        transition: opacity 0.1s ease-in;
    }
}
table.quote-list tr:hover td:last-child svg {
    opacity: 100%;
}
</style>

<script>
export default {
  props: {
    sceneIndex: {
      required: true,
      type: Number,
    },
    quotes: {
      required: true,
      type: Array,
    },
  },
  methods: {
    quote_link(quoteIndex) {
      return `/${this.$route.params.season}/${this.$route.params.episode}#${this.sceneIndex}-${quoteIndex}`;
    },
  },
};
</script>
