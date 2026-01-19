<script setup>
import { ref } from 'vue'

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['run'])

const code = ref(`import motor
from hub import port

motor.run(port.A, 1000)
`)

function handleRun() {
  emit('run', code.value)
}
</script>

<template>
  <div class="code-input">
    <h3>Code Input</h3>
    <textarea
      v-model="code"
      :disabled="disabled"
      placeholder="Enter your Python code here..."
      spellcheck="false"
    ></textarea>
    <button @click="handleRun" :disabled="disabled">
      {{ disabled ? 'Loading...' : 'Run Code' }}
    </button>
  </div>
</template>

<style scoped>
.code-input {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

h3 {
  margin: 0;
  color: #333;
}

textarea {
  width: 100%;
  height: 200px;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 14px;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
  background-color: #1e1e1e;
  color: #d4d4d4;
  line-height: 1.5;
}

textarea:focus {
  outline: none;
  border-color: #007acc;
}

textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007acc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover:not(:disabled) {
  background-color: #005a9e;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
