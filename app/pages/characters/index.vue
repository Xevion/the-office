<!-- <template>
  <div>
    <template v-if="ready">
      <BBreadcrumb v-if="ready" :items="breadcrumbs" />
      <BCard>
        <BListGroup>
          <BListGroupItem v-for="id in sorted_character_ids" :key="id">
            <BRow align-v="start" align-content="start">
              <BCol cols="5" md="4" lg="4" xl="3">
                <BImg
                  fluid-grow
                  class="rounded-sm"
                  :src="faceURL(id)"
                  :blank-src="faceURL(id, true)"
                  width="200"
                  height="200"
                  blank-width="200"
                  blank-height="200"
                />
              </BCol>
              <BCol>
                <h4>
                  {{ characters[id].name || id }}
                  <RouterLink
                    class="no-link"
                    :to="{ name: 'Character', params: { character: id } }"
                  >
                    <b-icon class="h6" icon="caret-right-fill" />
                  </RouterLink>
                  <span class="h6 font-italic" style="opacity: 50%">
                    {{ characters[id].actor }}
                  </span>
                </h4>
                <p class="pl-3">
                  {{ characters[id].summary }}
                </p>
              </BCol>
            </BRow>
          </BListGroupItem>
        </BListGroup>
      </BCard>
    </template>
    <template v-else>
      <BCard class="breadcrumb-skeleton mb-3">
        <Skeleton class="inlined" style="width: 10%" />
        <Skeleton class="inlined" style="width: 30%" />
      </BCard>
      <BCard>
        <BListGroup>
          <BListGroupItem v-for="i in 6" :key="i">
            <BRow align-v="start" align-content="start">
              <BCol cols="5" lg="4" xl="3">
                <ImageSkeleton style="width: 200px; height: 200px" />
              </BCol>
              <BCol>
                <Skeleton style="width: 40%; height: 2.7em" />
                <Skeleton style="width: 60%" />
                <Skeleton style="width: 25%" />
                <Skeleton style="width: 35%" />
                <Skeleton style="width: 60%" />
              </BCol>
            </BRow>
          </BListGroupItem>
        </BListGroup>
      </BCard>
    </template>
  </div>
</template>

<style lang="scss" scoped>
@use 'sass:color';
@use '@/scss/_variables.scss' as *;

h4 {
  .b-icon {
    font-size: 0.9rem;
    vertical-align: middle !important;
    position: relative;
    top: 3px;
    color: #007fe0;

    &:hover {
      color: color.adjust(#007fe0, $lightness: -10%);
    }
  }
}
</style>

<script lang="ts">
import { defineComponent } from 'vue';

import Skeleton from '@/components/common/Skeleton.vue';
import ImageSkeleton from '@/components/common/ImageSkeleton.vue';
import { BBreadcrumb, BImg } from 'bootstrap-vue-next';

export default defineComponent({
  name: 'CharactersComponent',

  components: {
    ImageSkeleton,
    Skeleton,
    BBreadcrumb,
    BImg,
  },

  computed: {
    ready() {
      return this.$store.getters.checkPreloaded('characters');
    },
    sorted_character_ids() {
      return this.$store.getters.getSortedCharacters();
    },
    characters() {
      return this.$store.state.characters;
    },
    breadcrumbs() {
      return [
        { text: 'Home', to: { name: 'Home' } },
        { text: 'Characters', active: true },
      ];
    },
  },

  async mounted() {
    await this.$store.dispatch(types.PRELOAD_CHARACTERS);

    // Re-compute computed properties since Vuex won't do it
    // this.$forceUpdate();
  },

  methods: {
    faceURL(character, thumbnail = false) {
      return `/img/${character}/` + (thumbnail ? 'face_thumb' : 'face') + '.jpeg';
    },
  },
});
</script>
-->


<script setup lang="ts"></script>
<template>
  <div>
    <h1>About</h1>
  </div>
</template>
