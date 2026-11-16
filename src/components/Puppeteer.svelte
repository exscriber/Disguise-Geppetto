<script lang="ts">
import { onMount } from 'svelte'
import { fade } from 'svelte/transition'
import { sleep, sleep_dev } from '@/lib/utils'
import type { LayerSettings, Personality } from '@/lib/types'

import Designer from './Director.svelte'
import LayerCard from './LayerCard.svelte'
import SafeButton from './SafeButton.svelte'

// TODO: alter signature for default import to work properly
// Most likely it will need new vite loader, not so shitty...
import { geppetto as PythonModule } from '@/lib/geppetto.py'
let python: ReturnType<typeof PythonModule>

const urlParams = new URLSearchParams(window.location.search)
let host = $state<string>(import.meta.env.VITE_D3 ?? urlParams.get('director') ?? 'localhost')

let isConnected = $state(false)
let isConnecting = $state(false)
const session = $derived(`http://${host}/api/session`)

let inProgress = $state(false)

// Mock - real data will came later from server
let videoSelected = $state(17)
let videoPersonalities = $state<Personality[]>([{ ver: 17, dmx: 81 }])
let colourPersonality = $state<Personality>({ ver: 1, dmx: 7 })

let videoSettings = $state<LayerSettings>({
  isEnabled: true,
  numLayers: 12,
  dmxAddress: '1 / 1',
  groupBy: 6,
})

let colorSettings = $state<LayerSettings>({
  isEnabled: false,
  numLayers: null,
  dmxAddress: '',
  groupBy: null,
})

onMount(() => connect(host))

async function connect(host: string) {
  console.log('Connecting to Director at', host)
  isConnected = false
  isConnecting = true

  try {
    python = PythonModule(host)
    await python.registration
    await update()
    isConnected = true
  } catch (error) {
    console.error('Error: Connection', error)
    isConnected = false
  } finally {
    await sleep_dev(2000)
    isConnecting = false
  }
}

async function update() {
  const result = await python.getPersonalityList('SockPuppetVideoModule')
  videoPersonalities = JSON.parse(result.returnValue)
  colourPersonality = JSON.parse((await python.getPersonality('ColourModule')).returnValue)
  console.log(`${videoPersonalities.length + 1} personalities loaded from d3 server`)
}

function handleReconnect() {
  console.log('Action: Reconnect button pressed')
  if (isConnecting) return console.log('Reject Reconnect: in progress already')

  connect(host)
}

async function handleReset() {
  console.log('Action: Reset button confirmed!')
  if (!isConnected) return console.log('Reject Reset: not connected yet')
  if (inProgress) return console.log('Reject Reset: in progress')
  await python.resetDmxPatch()
}

async function handlePatch() {
  console.log('Action: Patch button pressed')
  if (!isConnected) return console.log('Reject Patch: not connected yet')
  if (inProgress) return console.log('Reject Patch: in progress already')
  inProgress = true

  // Here’s steak goes...
  patchVideo: if (videoSettings.isEnabled) {
    const number = videoSettings.numLayers ?? 0
    const groupBy = videoSettings.groupBy ?? 0
    const { iver, dmx } = videoPersonalities.find((item) => item.ver === videoSelected)!
    let [univ, chan] = parseAddress(videoSettings.dmxAddress)

    if (!number || !dmx || !univ || !chan) {
      console.error('Error: something goes wrong with Video Settings...')
      break patchVideo
    }

    // Dry-aging layers in queue...
    const list = Array.from({ length: number }, (_, i) => {
      if (chan + dmx > 512) {
        chan = 1
        univ += 1
      }
      const entry = { univ, chan, name: `Video ${i + 1}` }
      chan += dmx
      return entry
    })

    // Chopping bite-sized chunks...
    const slices = []
    const chunkSize = groupBy >= 2 ? groupBy : list.length
    for (let i = 0; i < list.length; i += chunkSize) {
      slices.push(list.slice(i, i + chunkSize))
    }

    // Roasting d3 api medium rare...
    const cursor = parseFloat((await python.getCurrentTrackTime()).returnValue)
    for (const [index, chunk] of slices.entries()) {
      const layerUIDs = await Array.fromAsync(chunk, async (v) => {
        const r = await python.createNewLayer('Video', iver, v.name, v.univ, v.chan, cursor, 60)
        return r.returnValue
      })
      if (groupBy >= 2) await python.groupLayers(layerUIDs, `DMX Video ${index + 1}`)
    }
  }

  // Pretend we eat healthy today...
  patchColour: if (colorSettings.isEnabled) {
    const number = colorSettings.numLayers ?? 0
    const groupBy = colorSettings.groupBy ?? 0
    const { iver, dmx } = colourPersonality
    let [univ, chan] = parseAddress(colorSettings.dmxAddress)

    if (!number || !dmx || !univ || !chan) {
      console.error('Error: something goes wrong with Colour Settings...')
      break patchColour
    }

    // Checking lettuce still alive...
    const list = Array.from({ length: number }, (_, i) => {
      if (chan + dmx > 512) {
        chan = 1
        univ += 1
      }
      const entry = { univ, chan, name: `Colour ${i + 1}` }
      chan += dmx
      return entry
    })

    // Slicing n' Dicing with dull knife...
    const slices = []
    const chunkSize = groupBy >= 2 ? groupBy : list.length
    for (let i = 0; i < list.length; i += chunkSize) {
      slices.push(list.slice(i, i + chunkSize))
    }

    /// Seasoning with heavy api dressing...
    const cursor = parseFloat((await python.getCurrentTrackTime()).returnValue)
    for (const [index, chunk] of slices.entries()) {
      const layerUIDs = await Array.fromAsync(chunk, async (v) => {
        const r = await python.createNewLayer('Colour', iver, v.name, v.univ, v.chan, cursor, 60)
        return r.returnValue
      })
      if (groupBy >= 2) await python.groupLayers(layerUIDs, `DMX Colour ${index + 1}`)
    }
  }

  await sleep_dev(2000)
  inProgress = false
}

function parseAddress(address: string) {
  const regex = /^(\d{1,3})\D+(\d{1,3})$/
  const match = regex.exec(address.trim())
  if (!match) return [0, 0]
  const univ = Math.min(parseInt(match[1]), 256)
  const chan = Math.min(parseInt(match[2]), 512)
  return [univ, chan]
}
</script>

<div class="mx-auto flex w-md flex-col gap-4">
  <Designer bind:host status={isConnected} loading={isConnecting} onReconnect={handleReconnect} />
  <LayerCard
    label="Video Layers"
    bind:settings={videoSettings}
    bind:selected={videoSelected}
    personalities={videoPersonalities}
  />
  <LayerCard label="Colour Layers" bind:settings={colorSettings} />
  <section class="flex justify-center gap-3">
    <SafeButton label="Reset" onConfirm={handleReset} class="btn btn-outline btn-error w-36" />
    <button type="button" onclick={handlePatch} class="btn btn-outline btn-info w-36">
      <span>Patch</span>
      <span class="loading loading-bars" hidden={!inProgress}></span>
    </button>
  </section>
  {#if inProgress}
    <div class="mx-auto -mt-2 w-2/3" transition:fade>
      <progress class="progress progress-secondary"></progress>
    </div>
  {/if}
</div>
