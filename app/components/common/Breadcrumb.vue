<script setup lang="ts">
import {
  Breadcrumb,
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb';
import type { HTMLAttributes } from 'vue';
import { computed } from 'vue';

const lastIndex = computed(() => props.items.length - 1);

const props = defineProps<
  {
    items: { text: string; to?: string }[];
  } & { class?: HTMLAttributes['class'] }
>();
</script>

<template>
  <Breadcrumb :class="cn('w-full bg-gray-100 px-4 py-3', props.class)">
    <BreadcrumbList>
      <template v-for="(item, index) in items" :key="item.text">
        <BreadcrumbSeparator v-if="index !== 0" />
        <BreadcrumbItem>
          <BreadcrumbLink class="text-gray-600" as-child>
            <NuxtLink v-if="index !== lastIndex" :to="item.to">
              {{ item.text }}
            </NuxtLink>
            <span v-else>{{ item.text }}</span>
          </BreadcrumbLink>
        </BreadcrumbItem>
      </template>
    </BreadcrumbList>
  </Breadcrumb>
</template>
