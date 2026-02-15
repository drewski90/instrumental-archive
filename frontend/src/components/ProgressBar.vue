<template>
  <div class="progress-wrap">
    <input
      type="range"
      class="progress-slider"
      :max="player.duration"
      v-model="progress"
    />
  </div>
</template>

<script setup>
import { usePlayerStore } from '../stores/player'
import { computed } from 'vue'

const player = usePlayerStore()

const progress = computed({
  get: () => player.progress,
  set: (v) => {
    player.audio.currentTime = v
    player.progress = v
  }
})
</script>

<style scoped>
.progress-wrap{
  width:100%;
  padding:12px 12px;
}

/* base */
.progress-slider{
  width:100%;
  height:6px;
  appearance:none;
  border-radius:999px;
  background:
    linear-gradient(90deg,#2b7cff,#8a3cff);
  outline:none;
  box-shadow:
    0 0 10px rgba(120,150,255,.45),
    inset 0 0 8px rgba(0,0,0,.4);
}

/* thumb */
.progress-slider::-webkit-slider-thumb{
  appearance:none;
  width:18px;
  height:18px;
  border-radius:50%;
  background:radial-gradient(circle,#ffffff,#9db6ff);
  box-shadow:
    0 0 12px rgba(140,170,255,.8),
    0 0 20px rgba(140,170,255,.4);
  cursor:pointer;
}

.progress-slider::-moz-range-thumb{
  width:18px;
  height:18px;
  border-radius:50%;
  background:radial-gradient(circle,#ffffff,#9db6ff);
  box-shadow:
    0 0 12px rgba(140,170,255,.8),
    0 0 20px rgba(140,170,255,.4);
  cursor:pointer;
}
</style>
