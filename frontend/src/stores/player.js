import { defineStore } from 'pinia'
import api from '@/lib/api'


function createAudio() {
  const a = new Audio()
  a.crossOrigin = 'anonymous'
  return a
}

export const usePlayerStore = defineStore('player', {
  state: () => ({
    audio: createAudio(),

    audioCtx: null,
    analyser: null,
    source: null,

    currentTrack: null,
    currentIndex: 0,
    playing: false,
    queue: [],

    progress: 0,
    duration: 0,
    volume: 1
  }),

  actions: {

    init() {
      if (this.audioCtx) return

      this.audio.volume = this.volume

      this.audioCtx = new (window.AudioContext || window.webkitAudioContext)()

      this.source = this.audioCtx.createMediaElementSource(this.audio)
      this.analyser = this.audioCtx.createAnalyser()
      this.analyser.fftSize = 512

      this.source.connect(this.analyser)
      this.analyser.connect(this.audioCtx.destination)

      this.audio.addEventListener('timeupdate', () => {
        this.progress = this.audio.currentTime
        this.duration = this.audio.duration || 0
      })

      this.audio.addEventListener('ended', () => {
        this.next()
      })
    },

    setQueue(tracks) {
      this.queue = tracks
      this.currentIndex = 0
    },

    async play(track) {

  if (!this.audioCtx) this.init()

  if (track) {
    this.currentTrack = track

    // request presigned url
    const { data } = await api.get('/uploads/presign-get', {
      params: { key: track.SK }
    })

    this.audio.src = data.url
  }

  if (this.audioCtx.state !== 'running') {
    await this.audioCtx.resume()
  }

  await this.audio.play()
  this.playing = true
}
,

    async playFromQueue(index = 0) {
      if (!this.queue.length) return
      this.currentIndex = index
      await this.play(this.queue[this.currentIndex])
    },

    pause() {
      this.audio.pause()
      this.playing = false
    },

    toggle() {
      this.playing ? this.pause() : this.play()
    },

    next() {
      if (!this.queue.length) return
      this.currentIndex = (this.currentIndex + 1) % this.queue.length
      this.play(this.queue[this.currentIndex])
    },

    setVolume(v) {
      this.volume = v
      this.audio.volume = v
    }
  }
})
