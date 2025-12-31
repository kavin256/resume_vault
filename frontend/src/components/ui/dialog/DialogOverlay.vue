<script setup>
import { DialogOverlay } from "reka-ui";
import { cn } from "@/lib/utils.js";

const props = defineProps({
  asChild: { type: Boolean, required: false },
  as: { type: null, required: false },
  class: { type: null, required: false },
});
</script>

<template>
  <DialogOverlay
    :as="as"
    :as-child="asChild"
    :class="
      cn(
        'fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
        props.class
      )
    "
  >
    <slot />
  </DialogOverlay>
</template>
