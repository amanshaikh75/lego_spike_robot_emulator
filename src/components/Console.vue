<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  logs: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['clear'])

const consoleRef = ref(null)

// Auto-scroll to bottom when new logs are added
watch(
  () => props.logs.length,
  async () => {
    await nextTick()
    if (consoleRef.value) {
      consoleRef.value.scrollTop = consoleRef.value.scrollHeight
    }
  }
)

function handleClear() {
  emit('clear')
}
</script>

<template>
  <div class="console">
    <div class="console-header">
      <h3>Console Output</h3>
      <button @click="handleClear" class="clear-btn">Clear</button>
    </div>
    <div ref="consoleRef" class="console-output">
      <div v-if="logs.length === 0" class="placeholder">
        Console output will appear here...
      </div>
      <div v-for="(log, index) in logs" :key="index" class="log-entry">
        <span class="timestamp">[{{ log.timestamp }}]</span>
        <span class="message">{{ log.message }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.console {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.console-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h3 {
  margin: 0;
  color: #333;
}

.clear-btn {
  padding: 5px 10px;
  font-size: 12px;
  background-color: #666;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.clear-btn:hover {
  background-color: #555;
}

.console-output {
  height: 250px;
  overflow-y: auto;
  background-color: #1e1e1e;
  color: #d4d4d4;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px;
  padding: 12px;
  border-radius: 4px;
  border: 1px solid #333;
}

.placeholder {
  color: #666;
  font-style: italic;
}

.log-entry {
  margin-bottom: 4px;
  line-height: 1.4;
}

.timestamp {
  color: #888;
  margin-right: 8px;
}

.message {
  color: #d4d4d4;
}
</style>
