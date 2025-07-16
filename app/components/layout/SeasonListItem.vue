<script setup lang="ts">
import type { HTMLAttributes } from 'vue';
import { cn } from '@/lib/utils';
import useStore from '@/store';
import { ref } from 'vue';

const store = useStore();

const props = defineProps<
  {
    episodeNumber: number;
    seasonNumber: number;
    title: string;
  } & { class?: HTMLAttributes['class'] }
>();

const timeoutID = ref<ReturnType<typeof setTimeout> | null>(null);

const startHover = () => {
  timeoutID.value = setTimeout(() => {
    store.fetchEpisode({ season: props.seasonNumber, episode: props.episodeNumber });
  }, 500);
};

const stopHover = () => {
  if (timeoutID.value !== null) {
    clearTimeout(timeoutID.value);
    timeoutID.value = null;
  }
};
</script>

<template>
  <NuxtLink
    :id="`s-${seasonNumber}-ep-${episodeNumber}`"
    tabindex="0"
    :aria-label="`Episode ${episodeNumber}: ${title}`"
    :to="{ name: 'Episode', params: { season: seasonNumber, episode: episodeNumber } }"
    :class="
      cn(
        'group/item focus-visible:ring-ring focus-visible:bg-accent/50 ml-2 flex py-3 pr-3 pl-4 leading-6 transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
        props.class,
      )
    "
    @mouseover="startHover"
    @mouseleave="stopHover"
  >
    <span class="text-foreground/50 pr-2 select-none" :aria-hidden="true">{{
      episodeNumber.toString().padStart(2, '0')
    }}</span>
    <span class="text-foreground/80 group-hover/item:text-black">
      &OpenCurlyDoubleQuote;{{ title }}&CloseCurlyDoubleQuote;
    </span>
  </NuxtLink>
</template>

<style scoped></style>
