<script setup>
import { cn } from "@/lib/utils.js";

const props = defineProps({
  class: { type: null, required: false },
});
</script>

<template>
  <span
    role="link"
    aria-disabled="true"
    aria-current="page"
    :class="cn('font-normal text-foreground', props.class)"
  >
    <slot />
  </span>
</template>
