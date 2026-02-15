<template>
  <div class="d-flex justify-content-center align-items-center me-4">

    <button class="neon-btn me-2" @click="player.next()">
      <i class="bi bi-skip-forward-fill"></i>
    </button>

    <button class="neon-btn primary" @click="player.toggle()">
      <i :class="player.playing ? 'bi bi-pause-fill' : 'bi bi-play-fill'"></i>
    </button>

  </div>
</template>


<script setup>
import { usePlayerStore } from '../stores/player'
const player = usePlayerStore()
</script>

<style scoped>
.neon-btn i{
  font-size:20px;
  line-height:1;
}

.neon-btn{
  width:46px;
  height:46px;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:0;
  border-radius:50%;
}


/* hover */
.neon-btn:hover{
  transform: translateY(-2px);
  box-shadow:
    inset 0 0 12px rgba(120,150,255,0.35),
    0 0 18px rgba(120,150,255,0.45);
}

/* main play button */
.neon-btn.primary{
  background: linear-gradient(90deg,#2b7cff,#8a3cff);
  border:1px solid rgba(140,170,255,0.6);
  color:white;

  box-shadow:
    0 0 14px rgba(120,150,255,.55),
    0 0 28px rgba(120,150,255,.35);
}

.neon-btn.primary:hover{
  box-shadow:
    0 0 22px rgba(120,150,255,.75),
    0 0 40px rgba(120,150,255,.55);
}

</style>
