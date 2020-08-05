<template>
    <table class="quote-list mb-4 px-3 w-100">
        <tr v-for="(quote, index) in quotes" :key="`quote-${index}`">
            <td class="quote-speaker pl-3" v-if="quote.speaker">
                <span class="my-3">
                    {{ quote.speaker }}
                </span>
            </td>
            <td class="quote-text w-100">{{ quote.text }}</td>
        </tr>
    </table>
</template>

<style lang="scss">
    tr {
        &:not(:first-child) {
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
    }

    .quote-list > tr {
        white-space: nowrap;
    }

    .quote-text {
        white-space: normal;
    }

    .quote-speaker {
        /*min-width: 100px;*/
        padding-right: 1em;
        font-weight: 600;
        vertical-align: text-top;
        text-align: right;
    }
</style>

<script>
export default {
  props: ['quotes'],
};
</script>
