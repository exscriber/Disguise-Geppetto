<script lang="ts">
import { description } from '@/../package.json'
import Puppeteer from '@/components/Puppeteer.svelte'
</script>

<header class="navbar justify-center">
  <h1 class="text-2xl">{description}</h1>
</header>

<main>
  <Puppeteer />
</main>
