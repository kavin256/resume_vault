<script setup>
import { DialogPortal } from "reka-ui";

const props = defineProps({
  to: { type: [String, Object], required: false },
});
</script>

<template>
  <DialogPortal v-bind="props">
    <slot />
  </DialogPortal>
</template>
