<template>
    <div>
        <ais-hits>
            <div slot-scope="{ items }">
                <b-card v-for="item in items" :key="item.objectID" class="mb-1" body-class="p-0 py-2">
                    <b-card-text class="p-1 pl-2">
                        <strong>{{ item.speaker }}</strong>: {{ item.text }}
                    </b-card-text>
                </b-card>
            </div>
        </ais-hits>
    </div>
</template>
<style>
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
