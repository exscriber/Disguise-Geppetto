<script lang="ts">
interface Props {
  label?: string
  class?: string
  confirm?: string
  timeout?: number
  onConfirm: () => void
}

let {
  label,
  class: className,
  confirm = 'Are you sure?',
  timeout = 3000,
  onConfirm,
}: Props = $props()

let isConfirming = $state(false)

$effect(() => {
  if (!isConfirming) return
  const timer = setTimeout(() => (isConfirming = false), timeout)
  return () => clearTimeout(timer)
})

function handleClick() {
  if (isConfirming) {
    isConfirming = false
    onConfirm()
  } else {
    isConfirming = true
  }
}
</script>

<button
  type="button"
  class={className}
  class:danger={isConfirming}
  onclick={handleClick}
  onblur={() => (isConfirming = false)}
>
  {isConfirming ? confirm : label}
</button>

<style>
button.danger {
  background: var(--color-error);
  border-color: var(--color-error);
  color: var(--color-error-content);
}
</style>
