<script setup lang="ts">
import SeasonListItem from '@/components/layout/SeasonListItem.vue';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';
import { ChevronDown } from 'lucide-vue-next';
import { computed } from 'vue';

import episodes from '@/../public/json/episodes.json';

const data = computed(() => {
  return episodes.map((season, seasonIndex) => {
    return {
      seasonNumber: seasonIndex + 1,
      episodes: season.map((episode, episodeIndex) => {
        const title = episode?.title;
        if (!title) {
          // throw new Error(
          //   `Episode title is required for season ${seasonIndex + 1} episode ${episodeIndex + 1}`,
          // );
          return {
            episodeNumber: episodeIndex + 1,
            seasonNumber: seasonIndex + 1,
            title: 'IDK',
          };
        }

        return {
          episodeNumber: episodeIndex + 1,
          seasonNumber: seasonIndex + 1,
          title,
        };
      }),
    };
  });
});
</script>

<template>
  <Accordion type="single" class="font-roboto-slab ml-1 w-[300px]" collapsible>
    <AccordionItem
      v-for="season in data"
      :key="season.seasonNumber"
      :value="`season-${season.seasonNumber}`"
      class="group"
    >
      <AccordionTrigger
        :class="
          cn(
            'text-foreground/80 cursor-pointer border border-t-transparent bg-white/90 pr-6 pl-5 text-xl group-hover:border-zinc-400 hover:no-underline',
            season.seasonNumber !== 9 ? 'border-b-transparent' : 'border-b',
          )
        "
      >
        Season {{ season.seasonNumber }}
        <template #icon>
          <ChevronDown
            aria-hidden="true"
            class="text-muted-foreground pointer-events-none size-4 shrink-0 translate-y-1.5 transition-transform duration-200"
          />
        </template>
      </AccordionTrigger>
      <AccordionContent
        class="text-foreground/80 border-t border-r pb-0 group-hover:border-t-transparent"
      >
        <SeasonListItem
          v-for="episode in season.episodes"
          :key="`episode-${episode.title}`"
          class="bg-white/90 hover:bg-gray-100"
          :episode-number="episode.episodeNumber"
          :season-number="episode.seasonNumber"
          :title="episode.title"
        />
      </AccordionContent>
    </AccordionItem>
  </Accordion>
</template>
