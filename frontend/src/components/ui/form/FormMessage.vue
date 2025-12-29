<script setup>
import { computed } from "vue";
import { useFormField } from "./useFormField";
import { cn } from "@/lib/utils";

const props = defineProps({
  class: { type: null, required: false },
});

const { error, isTouched, formMessageId } = useFormField();

const body = computed(() =>
  isTouched && error.value?.message ? error.value.message : ""
);
</script>

<template>
  <p
    v-if="body"
    :id="formMessageId"
    :class="cn('text-sm font-medium text-destructive', props.class)"
  >
    {{ body }}
  </p>
</template>
