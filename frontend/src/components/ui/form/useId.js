let count = 0;

export function useId(deterministicId) {
  if (deterministicId) {
    return deterministicId;
  }
  count++;
  return `reka-${count}`;
}
