<template>
    <div>
        <ais-hits>
            <div slot-scope="{ items }">
                <SearchResult v-for="item in items" :item="item" :key="item.objectID"></SearchResult>
            </div>
        </ais-hits>
    </div>
</template>

<script>
import SearchResult from "./SearchResult.vue";

export default {
    name: "SearchResults",
    components: {
        SearchResult,
    },
};
</script>
