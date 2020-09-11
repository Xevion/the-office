<template>
    <table class="quote-list px-3 w-100">
        <tr
            v-for="(quote, index) in quotes"
            :key="`quote-${index}`"
            :id="`${sceneIndex}-${index}`"
            :class="
        $route.hash !== null &&
        $route.hash.substring(1) === `${sceneIndex}-${index}`
          ? 'highlight'
          : ''
      "
        >
            <td class="quote-speaker pl-3" v-if="quote.speaker">
        <span class="my-3">
          {{ quote.speaker }}
        </span>
            </td>
            <td class="quote-text w-100 pr-3">{{ quote.text }}</td>
            <td class="px-1 pl-2">
                <a :href="quote_link(index)" @click="copy(index)" class="no-link">
                    <b-icon icon="link45deg"></b-icon>
                </a>
            </td>
        </tr>
    </table>
</template>

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
        copy(quoteIndex) {
            this.$copyText(process.env.VUE_APP_BASE_URL + this.quote_link(quoteIndex))
        }
    },
};
</script>
