// ── API Service ────────────────────────────────────────────
// Talks to the FastAPI backend. Falls back to demo mode if backend is down.

const BASE_URL = '/api'  // proxied to http://localhost:8000 via vite.config.js

export async function generateDocument(userInput) {
  const res = await fetch(`${BASE_URL}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Request-ID': crypto.randomUUID(),
    },
    body: JSON.stringify({ input: userInput }),
    signal: AbortSignal.timeout(120_000), // 2-min timeout for long runs
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Server error ${res.status}`)
  }

  return res.json()
  // Returns: { doc_type, refined_topic, audience, agents_used, reasoning, result }
}

export async function checkHealth() {
  try {
    const res = await fetch(`${BASE_URL}/health`, { signal: AbortSignal.timeout(3000) })
    return res.ok
  } catch {
    return false
  }
}

export async function getHistory() {
  try {
    const res = await fetch(`${BASE_URL}/history`, { signal: AbortSignal.timeout(5000) })
    if (!res.ok) return []
    return res.json()
  } catch {
    return []
  }
}

// ── Streaming generate (uses Groq SSE endpoint) ────────────
// onToken(token: string) is called for every chunk that arrives.
// Throws if backend is unreachable so caller can fall back.
export async function generateDocumentStream(userInput, onToken) {
  const res = await fetch(`${BASE_URL}/generate/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ input: userInput }),
    signal: AbortSignal.timeout(120_000),
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Server error ${res.status}`)
  }

  const reader  = res.body.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const lines = decoder.decode(value, { stream: true }).split('\n')
    for (const line of lines) {
      if (!line.startsWith('data: ')) continue
      const data = line.slice(6).trim()
      if (data === '[DONE]') return
      try {
        const { token } = JSON.parse(data)
        if (token) onToken(token)
      } catch {
        // ignore malformed SSE lines
      }
    }
  }
}
