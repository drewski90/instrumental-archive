import { defineStore } from "pinia"
import api from "@/lib/api"

export const useInstrumentalsStore = defineStore("instrumentals", {

  state: () => ({
    items: [],
    cursor: null,
    loading: false,
    filters: {
      year: null,
      month: null,
      day: null
    }
  }),

  actions: {
    async toggleVisibility(key) {

      const resp = await api.patch("/uploads/toggle-visibility", { key })

      const updated = resp.data.item

      const idx = this.items.findIndex(i => i.SK === key)
      if (idx !== -1) {
        this.items[idx] = updated
      }

      return updated
    },

    async fetch({ reset = false } = {}) {

      if (this.loading) return
      this.loading = true

      if (reset) {
        this.items = []
        this.cursor = null
      }

      const params = {
        ...this.filters,
        cursor: this.cursor
      }

      const resp = await api.get("/uploads/list", { params })

      this.items.push(...resp.data.items)
      this.cursor = resp.data.cursor

      this.loading = false
    },

    setFilters(filters){
      this.filters = { ...this.filters, ...filters }
      this.fetch({ reset: true })
    }

  }
})
