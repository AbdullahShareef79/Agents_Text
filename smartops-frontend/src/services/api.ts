const API_BASE_URL = 'http://localhost:8000'

/**
 * Summarize text using the backend API
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
 * Extract and prioritize tasks from text using the backend API
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
 * @returns {Promise<{status: string}>}
 */
export async function healthCheck() {
  const response = await fetch(`${API_BASE_URL}/api/health`)
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }

  return await response.json()
}
