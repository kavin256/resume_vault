import { computed, inject } from "vue";
import {
  FORM_ITEM_INJECTION_KEY,
  FORM_FIELD_INJECTION_KEY,
} from "./injectionKeys";

export function useFormField() {
  const fieldContext = inject(FORM_FIELD_INJECTION_KEY);
  const fieldItemContext = inject(FORM_ITEM_INJECTION_KEY);

  const fieldState = computed(() => {
    const error = fieldContext?.errorMessage?.value;
    const isDirty = fieldContext?.meta?.value?.dirty;
    const isTouched = fieldContext?.meta?.value?.touched;
    const isValid = fieldContext?.meta?.value?.valid;

    return {
      invalid: !!error,
      isDirty: !!isDirty,
      isTouched: !!isTouched,
      error: { message: error },
      isValid: !!isValid,
    };
  });

  const formItemId = computed(() =>
    fieldItemContext?.id.value
      ? `${fieldItemContext.id.value}-form-item`
      : undefined
  );
  const formDescriptionId = computed(() =>
    fieldItemContext?.id.value
      ? `${fieldItemContext.id.value}-form-item-description`
      : undefined
  );
  const formMessageId = computed(() =>
    fieldItemContext?.id.value
      ? `${fieldItemContext.id.value}-form-item-message`
      : undefined
  );

  return {
    formItemId,
    formDescriptionId,
    formMessageId,
    ...fieldState.value,
  };
}
