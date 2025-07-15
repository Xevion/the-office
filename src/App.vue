<script setup lang="ts">
import SeasonList from '@/components/SeasonList.vue';
import { ref } from 'vue';
import logoSrc from '@/assets/logo.svg';

const sidebarOpen = ref(false);

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value;
};

const headings = [
  { name: 'Home', href: '/' },
  { name: 'Episodes', href: '/episodes' },
  { name: 'Characters', href: '/characters' },
  { name: 'Seasons', href: '/seasons' },
];
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header
      class="bg-white px-4 py-3 border-b border-gray-200 fixed top-0 left-0 right-0 z-40 flex items-center h-24"
    >
      <div class="flex items-center w-full justify-between">
        <div class="flex items-center space-x-4">
          <!-- Mobile menu button -->
          <button
            @click="toggleSidebar"
            class="lg:hidden p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
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
            <img :src="logoSrc" alt="The Office Logo" class="h-full max-w-[225px] py-4 mr-6" />
          </div>
        </div>

        <!-- Header Navigation -->
        <nav
          class="hidden text-gray-800 md:flex items-center space-x-2 font-display text-2xl tracking-widest lowercase"
        >
          <RouterLink
            v-for="heading in headings"
            :key="heading.name"
            :to="heading.href"
            class="hover:text-blue-600 px-3 py-2 transition-[color]"
          >
            {{ heading.name }}
          </RouterLink>
        </nav>

        <!-- Search bar -->
        <div class="hidden md:flex items-center">
          <div class="relative">
            <input
              type="text"
              placeholder="Search..."
              class="w-64 pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
            />
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg
                class="h-5 w-5 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="flex mt-24">
      <!-- Sidebar -->
      <div class="pl-8">
        <SeasonList />
      </div>

      <!-- Sidebar Overlay for mobile -->
      <div
        v-if="sidebarOpen"
        @click="toggleSidebar"
        class="fixed inset-0 z-20 bg-black bg-opacity-50 lg:hidden"
      ></div>

      <!-- Main Content -->
      <main class="col-span-8 lg:ml-0">
        <div class="p-6">
          <h2 class="text-2xl text-gray-900 mb-6">Welcome to The Office</h2>
          <p class="text-gray-600">
            This is your main content area. You can add your router-view or other components here.
          </p>
        </div>
      </main>
    </div>
  </div>
</template>
