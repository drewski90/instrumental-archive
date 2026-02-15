<template>
  <div>

    <div
      class="dropzone"
      @dragover.prevent
      @drop.prevent="onDrop"
      @click="openPicker"
    >
      Drag & drop audio files or click to upload

      <input
        ref="fileInput"
        type="file"
        multiple
        hidden
        accept="audio/*"
        @change="onSelect"
      />
    </div>

    <UploadItem
      v-for="item in uploads"
      :key="item.id"
      :file="item.file"
    />

  </div>
</template>

<script setup>
import { ref } from "vue"
import UploadItem from "./UploadItem.vue"

const uploads = ref([])
const fileInput = ref(null)

function openPicker(){
  fileInput.value?.click()
}

function onSelect(e){
  const files = Array.from(e.target.files || [])
  addFiles(files)
  e.target.value = ""   // allows selecting same files again
}

function onDrop(e){
  const files = Array.from(e.dataTransfer.files || [])
  addFiles(files)
}

function addFiles(files){
  files.forEach(f => {
    uploads.value.push({
      id: crypto.randomUUID(),
      file: f
    })
  })
}
</script>

<style scoped>
.dropzone{
  border:2px dashed #aaa;
  padding:60px;
  text-align:center;
  border-radius:12px;
  cursor:pointer;
}
</style>
