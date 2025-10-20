<template>
  <div>
    <header>
      <h1>SmartOps</h1>
      <p>Multi-Agent Text Analysis Pipeline</p>
      <p class="version">v2.0 - Parallel Agents + Feedback Loop</p>
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

        <div style="margin-top: 1rem; display: flex; gap: 1rem; flex-wrap: wrap;">
          <button @click="processWithAgents" :disabled="loading || !inputText.trim()" class="btn-primary">
            {{ loading ? 'Processing...' : '🚀 Process with Multi-Agent Pipeline' }}
          </button>
          <button @click="summarize" :disabled="loading || !inputText.trim()" class="btn-secondary">
            {{ loading ? 'Processing...' : 'Summarize Only' }}
          </button>
          <button @click="extractTasks" :disabled="loading || !inputText.trim()" class="btn-secondary">
            {{ loading ? 'Processing...' : 'Extract Tasks Only' }}
          </button>
          <button @click="clearAll" :disabled="loading" style="background-color: #666;">
            Clear All
          </button>
        </div>

        <div v-if="error" class="error" style="margin-top: 1rem;">
          {{ error }}
        </div>

        <!-- Run Metadata -->
        <div v-if="runMetadata" class="run-metadata">
          <div class="metadata-item">
            <strong>Run ID:</strong> {{ runMetadata.run_id.substring(0, 8) }}...
          </div>
          <div class="metadata-item">
            <strong>Quality:</strong> {{ (runMetadata.quality_score * 100).toFixed(0) }}%
          </div>
          <div class="metadata-item">
            <strong>Duration:</strong> {{ runMetadata.total_duration_ms.toFixed(0) }}ms
          </div>
          <div class="metadata-item" v-if="runMetadata.retry_count > 0">
            <strong>Retries:</strong> {{ runMetadata.retry_count }}
          </div>
        </div>
      </div>

      <SummaryList v-if="summary" :summary="summary" />
      <TaskTable v-if="tasks.length > 0" :tasks="tasks" />
      <AgentTimeline v-if="showTimeline" />
    </main>
  </div>
</template>

<script>
import { ref } from 'vue'
import SummaryList from './components/SummaryList.vue'
import TaskTable from './components/TaskTable.vue'
import AgentTimeline from './components/AgentTimeline.vue'
import { processText, summarizeText, extractTasks as apiExtractTasks } from './services/api'

export default {
  name: 'App',
  components: {
    SummaryList,
    TaskTable,
    AgentTimeline
  },
  setup() {
    const inputText = ref('')
    const summary = ref('')
    const tasks = ref([])
    const loading = ref(false)
    const error = ref('')
    const showTimeline = ref(false)
    const runMetadata = ref(null)

    const clearAll = () => {
      inputText.value = ''
      summary.value = ''
      tasks.value = []
      error.value = ''
      showTimeline.value = false
      runMetadata.value = null
    }

    const processWithAgents = async () => {
      loading.value = true
      error.value = ''
      summary.value = ''
      tasks.value = []
      showTimeline.value = false

      try {
        const result = await processText(inputText.value, 5)
        summary.value = result.summary
        tasks.value = result.tasks
        runMetadata.value = {
          run_id: result.run_id,
          quality_score: result.quality_score,
          total_duration_ms: result.total_duration_ms,
          retry_count: result.retry_count
        }
        showTimeline.value = true

        if (!summary.value && tasks.value.length === 0) {
          error.value = 'No results generated. Try with different text.'
        }
      } catch (err) {
        error.value = err.message || 'Failed to process text. Make sure the backend is running.'
      } finally {
        loading.value = false
      }
    }

    const summarize = async () => {
      loading.value = true
      error.value = ''
      summary.value = ''
      tasks.value = []
      showTimeline.value = false

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
      showTimeline.value = false

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
      showTimeline,
      runMetadata,
      processWithAgents,
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

header p.version {
  font-size: 0.875rem;
  color: #999;
  margin-top: 0.25rem;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.btn-primary {
  background-color: #1a73e8 !important;
  font-weight: 600;
}

.btn-primary:hover {
  background-color: #1557b0 !important;
}

.btn-secondary {
  background-color: #5f6368;
}

.btn-secondary:hover {
  background-color: #3c4043;
}

.run-metadata {
  margin-top: 1rem;
  padding: 1rem;
  background: #e8f5e9;
  border-radius: 8px;
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  font-size: 0.875rem;
}

.metadata-item {
  color: #333;
}

.metadata-item strong {
  color: #2e7d32;
  margin-right: 0.5rem;
}
</style>
