<template>
  <div>

    <h2 class="mb-4">Your Library</h2>

    <div class="table-responsive">
      <table class="table table-dark table-hover align-middle">

        <thead>
          <tr>
            <th style="width:60px;"></th>
            <th>Title</th>
            <th>Artist</th>
            <th style="width:120px;"></th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="track in library" :key="track.id">

            <td>
              <img :src="track.cover"
                   class="rounded"
                   style="width:48px;height:48px;object-fit:cover;">
            </td>

            <td>{{ track.title }}</td>
            <td class="text-secondary">{{ track.artist }}</td>

            <td>
              <button
                class="btn btn-light btn-sm"
                @click="player.play(track)"
              >
                Play
              </button>
            </td>

          </tr>
        </tbody>

      </table>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { usePlayerStore } from '@/stores/player'

const player = usePlayerStore()

const library = ref([
  {
    id: 1,
    title: "Dark Drill",
    artist: "Andrew",
    stream_url: "https://apmartinez-beats.s3.us-west-2.amazonaws.com/2022/March/5a39d909-6092-4af9-a0ed-3b2c10172a0e+-+79.mp3"
  },
  {
    id: 2,
    title: "Midnight Trap",
    artist: "Andrew",
    stream_url: "https://apmartinez-beats.s3.us-west-2.amazonaws.com/2022/March/d70c83e5-aabd-4e84-94d0-6fd0b55f994a+-+73_8.mp3"
  }
])
</script>
