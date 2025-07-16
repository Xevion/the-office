<script setup lang="ts">
import SeasonList from '@/components/layout/SeasonList.vue';
import { ref } from 'vue';
import logoSrc from '@/assets/logo.svg';
import SearchBar from '@/components/layout/SearchBar.vue';

const sidebarOpen = ref(false);

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value;
};

const headings = [
  { href: '/' },
  { name: 'Episodes', href: '/episodes' },
  { name: 'Characters', href: '/characters' },
  { name: 'Seasons', href: '/seasons' },
];
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header
      class="fixed top-0 right-0 left-0 z-40 flex h-24 items-center border-b border-gray-200 bg-white px-4 py-3"
    >
      <div class="flex w-full items-center justify-between">
        <div class="flex items-center space-x-4">
          <!-- Mobile menu button -->
          <button
            class="rounded-md p-2 text-gray-600 hover:bg-gray-100 hover:text-gray-900 focus:ring-2 focus:ring-blue-500 focus:outline-none focus:ring-inset lg:hidden"
            @click="toggleSidebar"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>

          <!-- Logo/Brand -->
          <div class="flex">
            <img :src="logoSrc" alt="The Office Logo" class="mr-6 h-full max-w-[225px] py-4" />
          </div>
        </div>

        <!-- Header Navigation -->
        <nav
          class="font-display hidden items-center space-x-2 text-2xl tracking-widest text-gray-800 lowercase md:flex"
        >
          <NuxtLink
            v-for="heading in headings"
            :key="heading.name"
            :to="heading.href"
            class="px-3 py-2 transition-[color] hover:text-blue-600"
          >
            {{ heading.name }}
          </NuxtLink>
        </nav>

        <!-- Search bar -->
        <div class="hidden items-center md:flex">
          <SearchBar />
        </div>
      </div>
    </header>

    <div class="mt-24 flex">
      <!-- Sidebar -->
      <div class="pl-8">
        <SeasonList />
      </div>

      <!-- Sidebar Overlay for mobile -->
      <div
        v-if="sidebarOpen"
        class="bg-opacity-50 fixed inset-0 z-20 bg-black lg:hidden"
        @click="toggleSidebar"
      />

      <!-- Main Content -->
      <main class="col-span-8 lg:ml-0">
        <NuxtPage />
      </main>
    </div>
  </div>
</template>
