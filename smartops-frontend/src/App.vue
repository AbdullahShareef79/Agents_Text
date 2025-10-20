<template>
  <div>
    <header>
      <h1>SmartOps</h1>
      <p>Text Summarization & Task Prioritization</p>
    </header>

    <main>
      <div class="card">
        <h2>Input Text</h2>
        <textarea
          v-model="inputText"
          placeholder="Paste or type your text here..."
          rows="10"
          style="width: 100%; margin-top: 1rem;"
        ></textarea>

        <div style="margin-top: 1rem; display: flex; gap: 1rem;">
          <button @click="summarize" :disabled="loading || !inputText.trim()">
            {{ loading ? 'Processing...' : 'Summarize' }}
          </button>
          <button @click="extractTasks" :disabled="loading || !inputText.trim()">
            {{ loading ? 'Processing...' : 'Extract & Prioritize Tasks' }}
          </button>
          <button @click="clearAll" :disabled="loading" style="background-color: #666;">
            Clear All
          </button>
        </div>

        <div v-if="error" class="error" style="margin-top: 1rem;">
          {{ error }}
        </div>
      </div>

      <SummaryList v-if="summary" :summary="summary" />
      <TaskTable v-if="tasks.length > 0" :tasks="tasks" />
    </main>
  </div>
</template>

<script>
import { ref } from 'vue'
import SummaryList from './components/SummaryList.vue'
import TaskTable from './components/TaskTable.vue'
import { summarizeText, extractTasks as apiExtractTasks } from './services/api'

export default {
  name: 'App',
  components: {
    SummaryList,
    TaskTable
  },
  setup() {
    const inputText = ref('')
    const summary = ref('')
    const tasks = ref([])
    const loading = ref(false)
    const error = ref('')

    const clearAll = () => {
      inputText.value = ''
      summary.value = ''
      tasks.value = []
      error.value = ''
    }

    const summarize = async () => {
      loading.value = true
      error.value = ''
      summary.value = ''
      tasks.value = []

      try {
        const result = await summarizeText(inputText.value)
        summary.value = result.summary
      } catch (err) {
        error.value = err.message || 'Failed to summarize text. Make sure the backend is running.'
      } finally {
        loading.value = false
      }
    }

    const extractTasks = async () => {
      loading.value = true
      error.value = ''
      summary.value = ''
      tasks.value = []

      try {
        const result = await apiExtractTasks(inputText.value)
        tasks.value = result.tasks
        if (tasks.value.length === 0) {
          error.value = 'No actionable tasks found in the text.'
        }
      } catch (err) {
        error.value = err.message || 'Failed to extract tasks. Make sure the backend is running.'
      } finally {
        loading.value = false
      }
    }

    return {
      inputText,
      summary,
      tasks,
      loading,
      error,
      summarize,
      extractTasks,
      clearAll
    }
  }
}
</script>

<style scoped>
header {
  text-align: center;
  margin-bottom: 2rem;
}

h1 {
  font-size: 2.5rem;
  color: #1a73e8;
  margin-bottom: 0.5rem;
}

header p {
  color: #666;
  font-size: 1.1rem;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #333;
}
</style>
