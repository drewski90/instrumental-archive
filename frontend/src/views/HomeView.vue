<template>
  <div>

    <h4 class="mb-4">Browse Instrumentals</h4>

    <div class="row g-2">
      <div
        v-for="(track, index) in tracks"
        :key="track.id"
        class="col-12 col-sm-6 col-md-4 col-lg-3"
      >
        <div
          class="card text-light"
          :class="{ 'active-track': player.currentIndex === index }"
        >

          <div class="card-body p-2">
            <div class="d-flex align-items-center justify-content-between">

              <div>
                <div class="h6 mb-0">{{ track.title }}</div>
                <div class="small">{{ track.lastModified }}</div>
              </div>

              <div class="d-flex align-items-center gap-2">

                <!-- Visibility toggle -->
                <button
                  v-if="auth.isAuthenticated"
                  class="btn btn-sm"
                  :class="track.visibility ? 'btn-success' : 'btn-outline-secondary'"
                  @click="store.toggleVisibility(track.SK)"
                >
                  <i :class="track.visibility ? 'bi bi-eye-fill' : 'bi bi-eye-slash'"></i>
                </button>

                <!-- Play / Pause -->
                <button
                  class="btn text-light btn-sm"
                  @click="togglePlay(index)"
                >
                  <i
                    :class="player.currentIndex === index && player.playing
                      ? 'bi bi-pause-fill'
                      : 'bi bi-play-fill'"
                  ></i>
                </button>

              </div>

            </div>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { usePlayerStore } from '@/stores/player'
import { useInstrumentalsStore } from '@/stores/instrumentals'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const player = usePlayerStore()
const store = useInstrumentalsStore()

const tracks = computed(() =>
  store.items.map(i => ({
    id: i.SK,
    SK: i.SK,
    title: i.metadata?.file_name,
    visibility: i.visibility ?? false,
    lastModified: formatDate(i.metadata?.last_modified)
  }))
)

onMounted(async () => {
  await store.fetch({ reset: true })
})

function togglePlay(index) {

  // clicking the currently playing track toggles pause/play
  if (player.currentIndex === index) {
    player.toggle()
    return
  }

  // otherwise play selected track
  player.playFromQueue(index)
}

function formatDate(ts) {
  if (!ts) return ''

  const d = new Date(Number(ts)) // supports epoch or ISO
  if (isNaN(d)) return ''

  return d.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

watch(
  tracks,
  (val) => {
    if (val.length) {
      player.setQueue(val)
    }
  },
  { immediate: true }
)
</script>
