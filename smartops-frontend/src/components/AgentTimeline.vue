<template>
  <div class="card agent-timeline">
    <h2>Agent Execution Timeline</h2>
    
    <div v-if="!runReport" class="no-data">
      <p>No execution data yet. Process some text to see the agent timeline.</p>
    </div>

    <div v-else class="timeline-container">
      <!-- Summary Stats -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Run ID</div>
          <div class="stat-value small">{{ runReport.run_id?.substring(0, 8) }}...</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Total Duration</div>
          <div class="stat-value">{{ runReport.total_duration_ms?.toFixed(0) }}ms</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Quality Score</div>
          <div class="stat-value">{{ (runReport.quality_score * 100).toFixed(0) }}%</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Retries</div>
          <div class="stat-value">{{ runReport.retry_count || 0 }}</div>
        </div>
      </div>

      <!-- Agent Timeline -->
      <div class="timeline">
        <div 
          v-for="(metric, index) in runReport.agent_timeline" 
          :key="index"
          class="timeline-item"
          :class="getStatusClass(metric.status)"
        >
          <div class="timeline-marker" :class="getStatusClass(metric.status)"></div>
          <div class="timeline-content">
            <div class="timeline-header">
              <span class="agent-name">{{ metric.agent_name }}</span>
              <span class="timeline-duration">{{ metric.duration_ms?.toFixed(1) }}ms</span>
            </div>
            <div class="timeline-details">
              <span class="timeline-status" :class="getStatusClass(metric.status)">
                {{ metric.status }}
              </span>
              <span v-if="metric.attempt > 1" class="timeline-attempt">
                Attempt {{ metric.attempt }}
              </span>
              <span class="timeline-time">
                {{ formatTime(metric.start_time) }}
              </span>
            </div>
            <div v-if="metric.error" class="timeline-error">
              {{ metric.error }}
            </div>
          </div>
        </div>
      </div>

      <!-- Feedback Section -->
      <div v-if="hasFeedback" class="feedback-section">
        <h3>Agent Feedback</h3>
        <div class="feedback-list">
          <div 
            v-for="(message, agent) in runReport.feedback" 
            :key="agent"
            class="feedback-item"
          >
            <strong>{{ agent }}:</strong> {{ message }}
          </div>
        </div>
      </div>

      <!-- Refresh Button -->
      <div class="timeline-actions">
        <button @click="refreshTimeline" class="btn-refresh">
          Refresh Timeline
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { getRunReport } from '../services/api'

export default {
  name: 'AgentTimeline',
  setup() {
    const runReport = ref(null)
    const loading = ref(false)

    const hasFeedback = computed(() => {
      return runReport.value?.feedback && Object.keys(runReport.value.feedback).length > 0
    })

    const refreshTimeline = async () => {
      loading.value = true
      try {
        const data = await getRunReport()
        if (!data.error) {
          runReport.value = data
        }
      } catch (err) {
        console.error('Failed to fetch run report:', err)
      } finally {
        loading.value = false
      }
    }

    const getStatusClass = (status) => {
      const statusMap = {
        'success': 'status-success',
        'failed': 'status-failed',
        'retrying': 'status-retrying',
        'skipped': 'status-skipped'
      }
      return statusMap[status] || 'status-unknown'
    }

    const formatTime = (timestamp) => {
      if (!timestamp) return ''
      const date = new Date(timestamp * 1000)
      return date.toLocaleTimeString('en-US', { 
        hour12: false, 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit',
        fractionalSecondDigits: 3
      })
    }

    // Auto-refresh on mount if there's data
    onMounted(() => {
      refreshTimeline()
    })

    return {
      runReport,
      loading,
      hasFeedback,
      refreshTimeline,
      getStatusClass,
      formatTime
    }
  }
}
</script>

<style scoped>
.agent-timeline {
  margin-top: 2rem;
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
}

.stat-label {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a73e8;
}

.stat-value.small {
  font-size: 1rem;
  font-family: monospace;
}

.timeline {
  position: relative;
  padding-left: 2rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 0.5rem;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #dee2e6;
}

.timeline-item {
  position: relative;
  margin-bottom: 1.5rem;
}

.timeline-marker {
  position: absolute;
  left: -1.5rem;
  top: 0.25rem;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #6c757d;
  border: 2px solid white;
  z-index: 1;
}

.timeline-marker.status-success {
  background: #28a745;
}

.timeline-marker.status-failed {
  background: #dc3545;
}

.timeline-marker.status-retrying {
  background: #ffc107;
}

.timeline-content {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1rem;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.agent-name {
  font-weight: 600;
  color: #333;
  font-size: 1rem;
}

.timeline-duration {
  font-family: monospace;
  color: #1a73e8;
  font-weight: 600;
}

.timeline-details {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  font-size: 0.875rem;
  color: #666;
}

.timeline-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: 500;
  text-transform: uppercase;
  font-size: 0.75rem;
}

.timeline-status.status-success {
  background: #d4edda;
  color: #155724;
}

.timeline-status.status-failed {
  background: #f8d7da;
  color: #721c24;
}

.timeline-status.status-retrying {
  background: #fff3cd;
  color: #856404;
}

.timeline-attempt {
  background: #e3f2fd;
  color: #1565c0;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.timeline-time {
  font-family: monospace;
  color: #999;
}

.timeline-error {
  margin-top: 0.5rem;
  padding: 0.5rem;
  background: #ffebee;
  color: #c62828;
  border-radius: 4px;
  font-size: 0.875rem;
}

.feedback-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #dee2e6;
}

.feedback-section h3 {
  margin-bottom: 1rem;
  color: #333;
}

.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.feedback-item {
  padding: 0.75rem;
  background: #e8f5e9;
  border-left: 4px solid #4caf50;
  border-radius: 4px;
  font-size: 0.875rem;
}

.feedback-item strong {
  color: #2e7d32;
}

.timeline-actions {
  margin-top: 1.5rem;
  text-align: center;
}

.btn-refresh {
  background-color: #6c757d;
  color: white;
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-refresh:hover {
  background-color: #5a6268;
}
</style>
