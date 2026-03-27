import { useState, useCallback, useRef } from 'react'
import { classifyInput } from '../data'
import { generateDocument, generateDocumentStream } from '../api'

export function useGenerate() {
  const [phase, setPhase]             = useState('idle')     // idle | routing | running | done | error
  const [route, setRoute]             = useState(null)
  const [activeAgent, setActiveAgent] = useState(-1)
  const [doneAgents, setDoneAgents]   = useState([])
  const [output, setOutput]           = useState(null)
  const [error, setError]             = useState(null)
  const [liveText, setLiveText]       = useState('')          // streaming tokens accumulate here
  const [isBackendLive, setIsBackendLive] = useState(false)

  // ── History: loaded from localStorage on first render ────
  const [history, setHistory] = useState(() => {
    try {
      const saved = localStorage.getItem('orion-history')
      return saved ? JSON.parse(saved) : []
    } catch {
      return []
    }
  })

  const abortRef = useRef(null)

  const simulateAgents = useCallback((agents, onDone) => {
    let i = 0
    setActiveAgent(0)
    setDoneAgents([])

    function step() {
      if (i >= agents.length) { onDone(); return }
      setActiveAgent(i)
      const delay = 800 + Math.random() * 700
      setTimeout(() => {
        setDoneAgents(prev => [...prev, i])
        i++
        if (i < agents.length) setActiveAgent(i)
        setTimeout(step, 200)
      }, delay)
    }
    setTimeout(step, 600)
  }, [])

  const submit = useCallback(async (userInput) => {
    if (!userInput.trim()) return

    setPhase('routing')
    setRoute(null)
    setOutput(null)
    setError(null)
    setLiveText('')
    setActiveAgent(-1)
    setDoneAgents([])

    // Classify input locally (instant keyword match)
    const detected = classifyInput(userInput)
    await new Promise(r => setTimeout(r, 900))   // brief routing animation pause
    setRoute(detected)
    setPhase('running')

    try {
      abortRef.current = new AbortController()

      // Start visual agent animation in parallel with API call
      simulateAgents(detected.agents, () => {})

      let backendResult = null
      let accumulated   = ''

      // ── 1. Try streaming (Groq) ───────────────────────────
      try {
        await generateDocumentStream(userInput, (token) => {
          accumulated += token
          setLiveText(accumulated)     // update live preview every token
        })
        backendResult = { result: accumulated }
        setIsBackendLive(true)

      } catch {
        // Streaming failed → try regular (CrewAI) endpoint
        setLiveText('')
        accumulated = ''
        try {
          backendResult = await generateDocument(userInput)
          setIsBackendLive(true)
        } catch {
          // Both failed → demo mode
          setIsBackendLive(false)
          await new Promise(r => setTimeout(r, detected.agents.length * 900 + 800))
        }
      }

      // Final result: backend → fallback (never use static sample outputs)
      const result = backendResult?.result
        ?? buildDemoOutput(userInput, detected)

      setLiveText('')                              // clear stream — final OutputCard takes over
      setActiveAgent(-1)
      setDoneAgents(detected.agents.map((_, i) => i))

      const docObj = {
        id:       Date.now(),
        input:    userInput,
        type:     detected.type,
        label:    detected.label,
        audience: detected.audience,
        agents:   detected.agents,
        result,
        ts:       new Date().toLocaleTimeString(),
      }

      setOutput(docObj)

      // ── Save history to localStorage ─────────────────────
      setHistory(prev => {
        const next = [docObj, ...prev].slice(0, 10)
        try { localStorage.setItem('orion-history', JSON.stringify(next)) } catch {}
        return next
      })

      setPhase('done')

    } catch (e) {
      if (e.name !== 'AbortError') {
        setLiveText('')
        setError(e.message)
        setPhase('error')
      }
    }
  }, [simulateAgents])

  const reset = useCallback(() => {
    abortRef.current?.abort()
    setPhase('idle')
    setRoute(null)
    setOutput(null)
    setError(null)
    setLiveText('')
    setActiveAgent(-1)
    setDoneAgents([])
  }, [])

  return {
    phase, route, activeAgent, doneAgents,
    output, error, history, isBackendLive, liveText,
    submit, reset,
  }
}

function buildDemoOutput(input, route) {
  return `# ${route.label}

**Your request:** ${input}

---

## Agent Pipeline Completed

${route.agents.map((a, i) => `**Step ${i + 1}: ${a}**
Completed research, analysis, and writing for this section.`).join('\n\n')}

---

## How to unlock real AI-generated documents

Add your **Groq API key** to \`backend/.env\` (free at console.groq.com) then run:

\`\`\`bash
cd backend
uvicorn main:app --reload --port 8000
\`\`\`

The Orion platform will stream fully AI-generated documents in real time.`
}
