<script setup lang="ts">
import { ref } from 'vue';
import { SearchIcon } from 'lucide-vue-next';

const searchQuery = ref('');
</script>

<template>
  <div class="relative">
    <input
      v-model="searchQuery"
      type="text"
      placeholder="Quotes, characters, episodes..."
      class="w-72 rounded-lg border border-gray-400 py-2 pr-4 pl-10 outline-none focus:border-transparent focus:ring-2 focus:ring-blue-500"
    >
    <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
      <SearchIcon class="size-5 text-gray-500" />
    </div>
  </div>
</template>
