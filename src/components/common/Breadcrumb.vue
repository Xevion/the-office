<script setup lang="ts">
import {
  Breadcrumb,
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb';
import type { HTMLAttributes } from 'vue';
import { cn } from '@/lib/utils';
import { computed } from 'vue';
import.meta.glob('/public/json/*.json');
console.log();

const lastIndex = computed(() => props.items.length - 1);

const props = defineProps<
  {
    items: { text: string; to: { name: string; params?: Record<string, string> } }[];
  } & { class?: HTMLAttributes['class'] }
>();
</script>

<template>
  <Breadcrumb :class="cn('w-full bg-gray-100 px-4 py-3', props.class)">
    <BreadcrumbList>
      <template v-for="(item, index) in items" :key="item.text">
        <BreadcrumbSeparator v-if="index !== 0" />
        <BreadcrumbItem>
          <BreadcrumbLink class="text-gray-600" :href="item.to.name" as-child>
            <RouterLink :to="item.to" v-if="index !== lastIndex">
              {{ item.text }}
            </RouterLink>
            <span v-else>{{ item.text }}</span>
          </BreadcrumbLink>
        </BreadcrumbItem>
      </template>
    </BreadcrumbList>
  </Breadcrumb>
</template>
