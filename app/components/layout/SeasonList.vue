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
import { cn } from '@/lib/utils';
import useStore from '@/store';

const store = useStore();
store.preloadEpisodes();
const seasons = computed(() => store.quoteData);
</script>

<template>
  <Accordion type="single" class="font-roboto-slab ml-1 w-[300px]" collapsible>
    <AccordionItem
      v-for="season in store.quoteData"
      :key="season.season_id"
      :value="`season-${season.season_id}`"
      class="group"
    >
      <AccordionTrigger
        :class="
          cn(
            'text-foreground/80 cursor-pointer border border-t-transparent bg-white/90 pr-6 pl-5 text-xl group-hover:border-zinc-400 hover:no-underline',
            season.season_id !== 9 ? 'border-b-transparent' : 'border-b',
          )
        "
      >
        Season {{ season.season_id }}
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
        <template v-for="(episode, index) in seasons[season.season_id - 1].episodes">
          <template v-if="'title' in episode">
            <SeasonListItem
              :key="`rl-${index}`"
              class="bg-white/90 hover:bg-gray-100"
              :episode-number="episode.episodeNumber"
              :season-number="episode.seasonNumber"
              :title="episode.title"
            />
          </template>
        </template>
      </AccordionContent>
    </AccordionItem>
  </Accordion>
</template>
