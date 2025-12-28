<script setup>
import { Field as VeeField } from "vee-validate";
import { provide, computed } from "vue";
import { FORM_FIELD_INJECTION_KEY } from "./injectionKeys";

const props = defineProps({
  name: { type: String, required: true },
  validateOnBlur: { type: Boolean, required: false, default: true },
  validateOnChange: { type: Boolean, required: false, default: true },
  validateOnInput: { type: Boolean, required: false, default: false },
  validateOnModelUpdate: { type: Boolean, required: false, default: true },
});
</script>

<template>
  <VeeField
    v-slot="{ field, errorMessage, meta }"
    :name="name"
    :validate-on-blur="validateOnBlur"
    :validate-on-change="validateOnChange"
    :validate-on-input="validateOnInput"
    :validate-on-model-update="validateOnModelUpdate"
  >
    <component
      :is="{
        setup() {
          provide(FORM_FIELD_INJECTION_KEY, {
            errorMessage: computed(() => errorMessage.value),
            meta: computed(() => meta),
          });
          return () => null;
        },
      }"
    />
    <slot :componentField="field" />
  </VeeField>
</template>
