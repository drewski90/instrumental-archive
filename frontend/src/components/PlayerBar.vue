<template>
  <footer class="px-3 py-4">
    <div class="d-flex justify-space-between">
        <ProgressBar />
        <PlayerControls />
    </div>
  </footer>
</template>

<script setup>
import PlayerControls from './PlayerControls.vue'
import ProgressBar from './ProgressBar.vue'
</script>

<style>
.player-dock{
  position:relative;
  z-index:5;

  /* glass blur */
  backdrop-filter: blur(18px) saturate(140%);
  -webkit-backdrop-filter: blur(18px) saturate(140%);

  /* translucent gradient so blur is visible */
  background: linear-gradient(
    to top,
    rgba(10,10,15,.75),
    rgba(10,10,15,.45)
  );

  /* subtle edge separation */
  border-top: 1px solid rgba(255,255,255,.08);

  /* soft glow edge */
  box-shadow:
    0 -8px 40px rgba(0,0,0,.35),
    inset 0 1px 0 rgba(255,255,255,.05);
}
.player-dock::after{
  content:"";
  position:absolute;
  top:0;
  left:0;
  right:0;
  height:1px;
  background:linear-gradient(90deg, transparent, rgba(255,255,255,.35), transparent);
  opacity:.35;
}

</style>