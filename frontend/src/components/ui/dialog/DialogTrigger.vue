<script setup>
import { DialogTrigger } from "reka-ui";
import { cn } from "@/lib/utils.js";

const props = defineProps({
  asChild: { type: Boolean, required: false },
  as: { type: null, required: false },
  class: { type: null, required: false },
});
</script>

<template>
  <DialogTrigger :as="as" :as-child="asChild" :class="cn(props.class)">
    <slot />
  </DialogTrigger>
</template>
