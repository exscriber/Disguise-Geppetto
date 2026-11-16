<script lang="ts">
import type { LayerSettings, Personality } from '@/lib/types'

interface Props {
  label: string
  settings: LayerSettings
  selected?: number
  personalities?: Personality[]
}

let { label, settings = $bindable(), selected = $bindable(), personalities = [] }: Props = $props()

let isNumValid = $derived(
  !settings.isEnabled || (settings.numLayers! > 0 && settings.numLayers! < 100),
)
let isGrpValid = $derived(
  !settings.isEnabled || !settings.groupBy || (settings.groupBy >= 2 && settings.groupBy < 100),
)
let isDmxValid = $derived.by(() => {
  const regex = /^\d{1,3}\D+\d{1,3}$/
  const trimmed = settings.dmxAddress.trim()
  return !settings.isEnabled || regex.test(trimmed)
})
</script>

<section class="card bg-base-200 border-base-content/30 border shadow-lg">
  <div class="card-body pt-4">
    <div class="mb-2 flex items-center justify-between">
      <h2 class="card-title">{label}</h2>
      <input
        type="checkbox"
        bind:checked={settings.isEnabled}
        class="toggle toggle-sm toggle-info"
      />
    </div>

    {#if personalities.length}
      <select
        bind:value={selected}
        class="select select-secondary bg-base-300 w-full appearance-none text-center"
      >
        <option disabled>Personality Version</option>
        {#each personalities as item (item.ver)}
          <option value={item.ver}>v{item.ver} - {item.dmx} channels</option>
        {/each}
      </select>
    {/if}

    <div class="flex items-center gap-2">
      <input
        type="number"
        bind:value={settings.numLayers}
        min="1"
        max="64"
        placeholder="N-layers"
        class="input bg-base-300 min-w-25 text-center font-mono"
        class:input-secondary={isNumValid}
        class:input-error={!isNumValid}
      />
      <span class="text-base-content/70 w-10 text-center">@</span>
      <input
        type="text"
        bind:value={settings.dmxAddress}
        placeholder="Univ.Chan"
        class="input bg-base-300 min-w-25 text-center font-mono"
        class:input-secondary={isDmxValid}
        class:input-error={!isDmxValid}
      />
      <span class="text-base-content/70 w-10 text-center font-bold">/</span>
      <input
        type="number"
        bind:value={settings.groupBy}
        min="2"
        max="16"
        placeholder="Group-By"
        class="input bg-base-300 min-w-25 text-center font-mono"
        class:input-secondary={isGrpValid}
        class:input-error={!isGrpValid}
      />
    </div>
  </div>
</section>
