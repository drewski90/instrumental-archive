<template>
  <div class="card p-3 mt-3">

    <div class="d-flex justify-content-between">
      <strong>{{ file.name }}</strong>
      <span>{{ progress }}%</span>
    </div>

    <div class="progress mt-2">
      <div class="progress-bar" :style="{ width: progress + '%' }"></div>
    </div>

  </div>
</template>

<script setup>
import api from "@/lib/api"
import { ref, onMounted } from "vue"

const props = defineProps({
  file: File
})

const progress = ref(0)

onMounted(upload)

async function upload(){

  // EXACT backend contract — nothing extra
  const payload = {
    file_name: props.file.name,
    last_modified: String(props.file.lastModified),
    content_type: props.file.type
  }

  // Step 1: presign
  const presign = await api.post("/uploads/presign", payload)
  const { url, fields } = presign.data.upload

  // Step 2: direct S3 POST
  const form = new FormData()
  Object.entries(fields).forEach(([k,v]) => form.append(k, v))
  form.append("file", props.file)
  form.append("Content-Type", props.file.type)

  await api.post(url, form, {
    onUploadProgress: e => {
      progress.value = Math.round((e.loaded * 100) / e.total)
    }
  })
}
</script>
