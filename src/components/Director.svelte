<script lang="ts">
interface Props {
  label?: string
  host?: string
  status?: boolean
  loading?: boolean
  onReconnect: () => void
}

let {
  label = 'Director connection',
  host = $bindable('127.0.0.1:80'),
  status = false,
  loading = false,
  onReconnect,
}: Props = $props()
</script>

<section class="card bg-base-200 border-base-content/30 border shadow-lg">
  <div class="card-body pt-4">
    <div class="mb-2 flex items-center justify-between">
      <h2 class="card-title">{label}</h2>
      <span
        class="badge w-20 {status
          ? 'bg-success/20 text-success border-success/50'
          : 'bg-error/20 text-error border-error/50'}"
      >
        {status ? 'online' : 'offline'}
      </span>
    </div>

    <div class="flex items-center gap-3">
      <input
        type="text"
        bind:value={host}
        placeholder="d3 address"
        class="input input-secondary bg-base-300 w-full text-center font-mono"
      />
      <button
        type="button"
        onclick={onReconnect}
        aria-label="Reconnect"
        class="btn btn-outline btn-info"
      >
        <span class="swap swap-rotate" class:swap-active={loading}>
          <span class="swap-on loading loading-bars"></span>
          <span class="swap-off">
            <svg viewBox="0 0 24 24" stroke="currentColor" fill="none" class="h-6 w-6">
              <path
                stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
          </span>
        </span>
      </button>
    </div>
  </div>
</section>
