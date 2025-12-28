<script setup>
import { Slot } from "reka-ui";
import { computed, provide } from "vue";
import { FORM_ITEM_INJECTION_KEY } from "./injectionKeys";
import { useId } from "./useId";

const props = defineProps({
  class: { type: null, required: false },
});

const id = useId();

provide(FORM_ITEM_INJECTION_KEY, {
  id: computed(() => id),
});
</script>

<template>
  <Slot :class="props.class">
    <slot />
  </Slot>
</template>
