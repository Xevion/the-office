<template>
    <div>
        <ais-hits>
            <div slot-scope="{ items }">
                <SearchResult
                    v-for="item in items"
                    :item="item"
                    :key="item.objectID"
                ></SearchResult>
            </div>
        </ais-hits>
    </div>
</template>
<style lang="scss">
.card-footer {
    padding: 0.1em;
    font-size: 0.8em;
    color: grey;
}

mark,
.mark {
    padding: 0.02em;
    background-color: $highlight;
    /*color: #black;*/
    /*-webkit-filter: invert(100%);*/
    /*filter: invert(100%);*/
}

.ais-Hits-item,
.ais-InfiniteHits-item,
.ais-InfiniteResults-item,
.ais-Results-item {
    /*margin-top: 1rem;*/
    /*margin-left: 1rem;*/
    /*padding: 1rem;*/
    /*width: calc(25% - 1rem);*/
    border: none;
    box-shadow: none;
}
</style>
<script>
import SearchResult from "./SearchResult.vue";

export default {
    name: "SearchResults",
    components: {
        SearchResult,
    },
};
</script>
