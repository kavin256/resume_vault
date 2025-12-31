<script setup>
import { toValue } from "vue";
import { useFormField } from "./useFormField";
import { cn } from "@/lib/utils.js";

defineOptions({
  inheritAttrs: false,
});

const { error, isTouched, formItemId, formDescriptionId, formMessageId } =
  useFormField();
</script>

<template>
  <input
    :id="formItemId"
    :class="
      cn(
        'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
        error && isTouched && 'border-red-500',
        $attrs.class ?? ''
      )
    "
    :aria-describedby="
      !error ? `${formDescriptionId}` : `${formDescriptionId} ${formMessageId}`
    "
    :aria-invalid="!!error"
    v-bind="{ ...$attrs, class: undefined }"
  />
</template>
