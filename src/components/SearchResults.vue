<template>
    <div>
        <ais-hits>
            <template v-slot="{ items }">
<div>
                <SearchResult v-for="item in items" :key="item.objectID" :item="item" />
            </div>
</template>
        </ais-hits>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import SearchResult from "@/components/SearchResult.vue";

export default defineComponent({
  name: "SearchResults",

  components: {
      SearchResult,
  },
});
</script>
