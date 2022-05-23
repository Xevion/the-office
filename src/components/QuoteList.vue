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
                <DynamicSpeaker v-if="quote.isAnnotated" :text="quote.speaker" :characters="quote.characters" class="my-3" />
                <router-link v-else :to="{name: 'Character', params: {character: quote.character}}" class="speaker-link">
                    {{ quote.speaker }}
                </router-link>
            </td>
            <td class="quote-text w-100 pr-3" v-html="transform(quote.text)" />
            <td class="px-1 pl-2">
                <a :href="quote_link(index)" class="no-link" @click="copy(index)">
                    <b-icon icon="link45deg" />
                </a>
            </td>
        </tr>
    </table>
</template>

<style lang="scss">
.speaker-bg {
    color: $grey-8;
}

.speaker-link {
    &, &:hover {
        color: $grey-10;
        cursor: pointer;
        text-decoration: none;
    }
}
</style>

<script>
import DynamicSpeaker from "@/components/DynamicSpeaker";

export default {
    components: {
        DynamicSpeaker
    },
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
        transform(quoteText) {
            if (quoteText.includes("[")) {
                return quoteText.replace(/\[([^\]]+)]/g, ' <i>[$1]</i> ')
            }
            return quoteText
        },
        quote_link(quoteIndex) {
            return `/${this.$route.params.season}/${this.$route.params.episode}#${this.sceneIndex}-${quoteIndex}`;
        },
        copy(quoteIndex) {
            this.$copyText(process.env.VUE_APP_BASE_URL + this.quote_link(quoteIndex))
        }
    },
};
</script>
