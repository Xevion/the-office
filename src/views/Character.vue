<template>
  <div>
    <BBreadcrumb v-if="ready" :items="breadcrumbs" />
    <BCard v-else class="breadcrumb-skeleton mb-3">
      <Skeleton style="width: 40%"></Skeleton>
    </BCard>
    <BCard>
      <h4 v-if="ready">{{ character?.name }}</h4>
      <Skeleton v-else style="max-width: 30%"></Skeleton>
      <BCard-body v-if="ready">
        {{ character?.summary }}
      </BCard-body>
    </BCard>
  </div>
</template>

<style lang="scss" scoped>
@use '@/scss/_variables.scss' as *;

.breadcrumb-skeleton {
  background-color: $gray-100;
  height: 48px;

  & > .card-body {
    padding: 0 0 0 1em;
    display: flex;
    align-items: center;
  }
}
</style>

<script lang="ts">
import { defineComponent, nextTick } from 'vue';
import Skeleton from '@/components/common/Skeleton.vue';
import { BBreadcrumb } from 'bootstrap-vue-next';
import useStore from '@/store';

interface BreadcrumbItem {
  text: string;
  to?: { name: string };
  active?: boolean;
}

export default defineComponent({
  name: 'CharacterPage',

  components: {
    Skeleton,
    BBreadcrumb,
  },

  setup() {
    const store = useStore();
    return {
      store,
    };
  },
  computed: {
    character() {
      return this.store.characters[this.$route.params.character as string];
    },
    ready(): boolean {
      return this.character !== undefined;
    },

    breadcrumbs(): BreadcrumbItem[] {
      return [
        {
          text: 'Home',
          to: { name: 'Home' },
        },
        {
          text: 'Characters',
          to: { name: 'Characters' },
        },
        {
          text: this.character?.name || (this.$route.params.character as string),
          active: true,
        },
      ];
    },
  },

  watch: {
    '$route.params.character'() {
      nextTick(() => {
        this.fetchCharacter();
      });
    },
  },

  mounted() {
    this.fetchCharacter();
  },

  methods: {
    async fetchCharacter(): Promise<void> {
      try {
        await this.store.preloadCharacters();
        this.character = this.store.characters[this.$route.params.character as string];
      } catch (error) {
        console.error('Error fetching character:', error);
      }
    },
  },
});
</script>
