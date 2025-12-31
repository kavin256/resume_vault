<script setup>
import { cn } from "@/lib/utils.js";

const props = defineProps({
  class: { type: null, required: false },
});
</script>

<template>
  <tr
    :class="
      cn(
        'border-b border-gray-200 transition-colors hover:bg-gray-50 data-[state=selected]:bg-gray-50',
        props.class
      )
    "
  >
    <slot />
  </tr>
</template>
