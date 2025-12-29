<script setup>
import { Slot } from "reka-ui";
import { cn } from "@/lib/utils";

const props = defineProps({
  class: { type: null, required: false },
});
</script>

<template>
  <nav aria-label="breadcrumb" :class="cn('relative break-words', props.class)">
    <slot />
  </nav>
</template>
