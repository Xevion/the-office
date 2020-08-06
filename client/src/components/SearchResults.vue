<template>
    <div>
        <ais-hits>
            <div slot-scope="{ items }">
                <b-card v-for="item in items" :key="item.objectID" class="mb-1" body-class="p-0 py-2">
                    <b-card-text class="p-1 pl-2">
                        <strong v-html="item._highlightResult.speaker.value"></strong>:
                        <span v-html="item._highlightResult.text.value" class="pl-1"></span>
                        <!--                        <strong>{{ item.speaker }}</strong>:-->
                        <!--                        <ais-highlight attribute="text" :hit="item"/>-->
                    </b-card-text>
                    <template v-slot:footer>
                        <router-link class="no-link" :to="`/${item.season}/${item.episode}#${item.section}`">
                            Season {{ item.season }} Episode {{ item.episode }} Scene {{ item.section }}
                        </router-link>
                    </template>
                </b-card>
            </div>
        </ais-hits>
    </div>
</template>
<style>
    .card-footer {
        padding: 0.1em;
        font-size: 0.8em;
        color: grey;
    }

    mark, .mark {
        padding: 0.02em;
        background-color: #fff500;
        /*color: #black;*/
        /*-webkit-filter: invert(100%);*/
        /*filter: invert(100%);*/
    }

    .ais-Hits-item, .ais-InfiniteHits-item, .ais-InfiniteResults-item, .ais-Results-item {
        /*margin-top: 1rem;*/
        /*margin-left: 1rem;*/
        /*padding: 1rem;*/
        /*width: calc(25% - 1rem);*/
        border: none;
        box-shadow: none;
    }
</style>
<script>
export default {
  name: 'SearchResults',
};
</script>
