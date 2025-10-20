<template>
  <div class="card">
    <h2>Prioritized Tasks</h2>
    <p style="color: #666; margin-bottom: 1rem;">{{ tasks.length }} task(s) found</p>
    
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Priority</th>
            <th>Task</th>
            <th>Owner</th>
            <th>Due Date</th>
            <th>Effort</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(task, index) in tasks" :key="index">
            <td>
              <span class="priority-badge" :class="getPriorityClass(task.priority_score)">
                {{ task.priority_score }}
              </span>
            </td>
            <td class="task-text">{{ task.task }}</td>
            <td>
              <span v-if="task.owner" class="owner-badge">{{ task.owner }}</span>
              <span v-else class="not-assigned">—</span>
            </td>
            <td>
              <span v-if="task.due_date" class="due-date">{{ formatDate(task.due_date) }}</span>
              <span v-else class="not-assigned">—</span>
            </td>
            <td>
              <span class="effort-badge" :class="getEffortClass(task.effort_estimate)">
                {{ task.effort_estimate }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TaskTable',
  props: {
    tasks: {
      type: Array,
      required: true
    }
  },
  methods: {
    getPriorityClass(score) {
      if (score >= 80) return 'priority-high'
      if (score >= 60) return 'priority-medium'
      return 'priority-low'
    },
    getEffortClass(effort) {
      return `effort-${effort}`
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      const today = new Date()
      const tomorrow = new Date(today)
      tomorrow.setDate(tomorrow.getDate() + 1)
      
      // Check if it's today or tomorrow
      if (date.toDateString() === today.toDateString()) {
        return 'Today'
      } else if (date.toDateString() === tomorrow.toDateString()) {
        return 'Tomorrow'
      }
      
      // Otherwise return formatted date
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    }
  }
}
</script>

<style scoped>
.table-container {
  overflow-x: auto;
  margin-top: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

th {
  background-color: #f8f9fa;
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #dee2e6;
  color: #495057;
}

td {
  padding: 0.75rem;
  border-bottom: 1px solid #dee2e6;
}

tr:hover {
  background-color: #f8f9fa;
}

.task-text {
  max-width: 400px;
  word-wrap: break-word;
}

.priority-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.875rem;
}

.priority-high {
  background-color: #ffebee;
  color: #c62828;
}

.priority-medium {
  background-color: #fff3e0;
  color: #e65100;
}

.priority-low {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.owner-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background-color: #e3f2fd;
  color: #1565c0;
  border-radius: 4px;
  font-size: 0.875rem;
}

.effort-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: capitalize;
}

.effort-low {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.effort-medium {
  background-color: #fff3e0;
  color: #e65100;
}

.effort-high {
  background-color: #ffebee;
  color: #c62828;
}

.due-date {
  color: #495057;
  font-size: 0.875rem;
}

.not-assigned {
  color: #adb5bd;
}
</style>
