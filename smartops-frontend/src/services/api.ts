const API_BASE_URL = 'http://localhost:8000'

/**
 * Process text through multi-agent pipeline (NEW v2.0 endpoint)
 * @param {string} text - The text to process
 * @param {number} numSentences - Number of sentences for summary
 * @returns {Promise<{summary: string, tasks: Array, run_id: string, quality_score: number, total_duration_ms: number, retry_count: number}>}
 */
export async function processText(text, numSentences = 5) {
  const response = await fetch(`${API_BASE_URL}/api/process`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text, num_sentences: numSentences }),
  })

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  return await response.json()
}

/**
 * Get the latest run report with agent timeline
 * @returns {Promise<{run_id: string, agent_timeline: Array, quality_score: number, ...}>}
 */
export async function getRunReport() {
  const response = await fetch(`${API_BASE_URL}/api/run-report`)
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  return await response.json()
}

/**
 * Summarize text using the backend API (LEGACY - kept for backward compatibility)
 * @param {string} text - The text to summarize
 * @returns {Promise<{summary: string}>}
 */
export async function summarizeText(text) {
  const response = await fetch(`${API_BASE_URL}/api/summarize`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  })

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  return await response.json()
}

/**
 * Extract and prioritize tasks from text using the backend API (LEGACY)
 * @param {string} text - The text to extract tasks from
 * @returns {Promise<{tasks: Array}>}
 */
export async function extractTasks(text) {
  const response = await fetch(`${API_BASE_URL}/api/tasks/priority`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  })

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  return await response.json()
}

/**
 * Check backend health
 * @returns {Promise<{status: string, version: string}>}
 */
export async function healthCheck() {
  const response = await fetch(`${API_BASE_URL}/api/health`)
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  return await response.json()
}
