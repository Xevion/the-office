<template>
    <div class="image-skeleton" />
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: "ImageSkeleton",
});
</script>

<style lang="scss">
@use "@/scss/_variables.scss" as *;

.image-skeleton {
    width: 100%;
    height: 100%;
    background-color: $gray-400;
    display: block;
    border-radius: 3px;
}

</style>
