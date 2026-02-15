<template>
  <div class="app-root d-flex">

    <!-- RIGHT MAIN AREA -->
    <div class="main-area flex-grow-1 d-flex flex-column">

      <!-- Background -->
      <canvas ref="bgCanvas" class="bg-canvas"></canvas>

      <AppNavbar />

      <!-- SCROLLING CONTENT -->
      <main class="content-scroll flex-grow-1 container py-4">
        <router-view />
      </main>

      <!-- PLAYER AT BOTTOM (not fixed) -->
      <PlayerBar class="player-bar" v-if="player.queue.length > 0"/>

    </div>

  </div>
</template>



<script setup>
import { onMounted, ref } from 'vue'
import { usePlayerStore } from './stores/player'
import PlayerBar from '@/components/PlayerBar.vue'
import AppNavbar from './components/AppNavbar.vue'
import { startVisualizer } from '@/services/visualizerEngine'
import { useInstrumentalsStore } from "@/stores/instrumentals"
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const player = usePlayerStore()
const store = useInstrumentalsStore()
const bgCanvas = ref(null)

onMounted(async () => {
  startVisualizer(bgCanvas.value)  // start WebGL visualizer
  await store.fetch({ reset: true })
  player.init()                 // initialize audio engine
})
</script>

<style>


/* Background canvas */
.bg-canvas {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

/* UI sits above canvas */
.content-layer {
  position: relative;
  z-index: 2;
}

/* Player fixed bottom */
.player-fixed {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 5;
}

.app-root{
  position:relative;
  overflow:hidden;
}

/* left rail */
.brand-rail{
  width:80px;
  min-width:50px;
  padding:5px;
  height:100vh;

  display:flex;
  align-items:center;
  justify-content:center;

  z-index:4;
}

/* svg fills column */
.brand-svg{
  width:100%;
  height:100%;
  text-transform: capitalize;
  color: white;
}

/* text styling */
.brand-text{
  fill:#ffffff;
  text-transform: uppercase;
  font-size:80px;
  font-weight:600;
  letter-spacing:6px;
  font-family: Inter, sans-serif;
  opacity:.85;
}

/* background canvas stays full viewport */
.bg-canvas{
  position:fixed;
  inset:0;
  width:100%;
  height:100%;
  z-index:0;
}

.content-layer{
  position:relative;
  z-index:2;
}

.player-fixed{
  position:fixed;
  bottom:0;
  left:80px;   /* aligns with rail */
  right:0;
  z-index:5;
}

.app-root{
  height:100vh;
  overflow:hidden;
  color: white;
}

/* right side column */
.main-area{
  position:relative;
  height:calc(100vh-67px);
  margin-top: 65px;
}

/* scrolling content */
.content-scroll{
  overflow-y:auto;
  position:relative;
  z-index:2;
}

/* player sits naturally at bottom */
.player-bar{
  position:relative;
  z-index:3;
}

/* background canvas still viewport-wide */
.bg-canvas{
  position:fixed;
  inset:0;
  width:100%;
  height:100%;
  z-index:0;
}

.card {
  background-color: rgba(24, 0, 113, 0.667) !important;
  color: white !important;
}
.card.active-track {
  background: rgba(80,140,255,0.25);
  border-color: rgba(120,170,255,0.6);
  backdrop-filter: blur(10px);
}
</style>
