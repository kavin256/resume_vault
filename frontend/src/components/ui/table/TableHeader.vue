<script setup>
import { cn } from "@/lib/utils.js";

const props = defineProps({
  class: { type: null, required: false },
});
</script>

<template>
  <thead :class="cn('bg-gray-50 [&_tr]:border-b border-gray-200', props.class)">
    <slot />
  </thead>
</template>
