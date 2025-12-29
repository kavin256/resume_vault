<script setup>
import { Field as VeeField } from "vee-validate";
import { provide, toRef } from "vue";
import { FORM_FIELD_INJECTION_KEY } from "./injectionKeys";

const props = defineProps({
  name: { type: String, required: true },
  validateOnBlur: { type: Boolean, required: false, default: false },
  validateOnChange: { type: Boolean, required: false, default: false },
  validateOnInput: { type: Boolean, required: false, default: false },
  validateOnModelUpdate: { type: Boolean, required: false, default: false },
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
    <FieldProvider :error-message="errorMessage" :meta="meta">
      <slot :componentField="field" />
    </FieldProvider>
  </VeeField>
</template>

<script>
import { defineComponent, provide, toRef } from "vue";
import { FORM_FIELD_INJECTION_KEY } from "./injectionKeys";

const FieldProvider = defineComponent({
  name: "FieldProvider",
  props: {
    errorMessage: { type: String },
    meta: { type: Object },
  },
  setup(props) {
    provide(FORM_FIELD_INJECTION_KEY, {
      errorMessage: toRef(props, "errorMessage"),
      meta: toRef(props, "meta"),
    });
  },
  render() {
    return this.$slots.default?.();
  },
});

export { FieldProvider };
</script>
