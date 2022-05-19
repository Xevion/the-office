<template>
    <table class="quote-list px-3 w-100">
        <tr
            v-for="(quote, index) in quotes"
            :id="`${sceneIndex}-${index}`"
            :key="`quote-${index}`"
            :class="
                $route.hash !== null &&
                    $route.hash.substring(1) === `${sceneIndex}-${index}`
                    ? 'highlight'
                    : ''
            "
        >
            <td v-if="quote.speaker" class="quote-speaker pl-3">
                <span class="my-3">
                    {{ quote.speaker }}
                </span>
            </td>
            <td class="quote-text w-100 pr-3">
                {{ quote.text }}
            </td>
            <td class="px-1 pl-2">
                <a :href="quote_link(index)" class="no-link" @click="copy(index)">
                    <b-icon icon="link45deg" />
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
