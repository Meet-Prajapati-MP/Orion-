import { useEffect, useRef } from 'react'
import Header        from './components/Header'
import Hero          from './components/Hero'
import InputBox      from './components/InputBox'
import AgentPipeline from './components/AgentPipeline'
import OutputCard    from './components/OutputCard'
import CapabilityGrid from './components/CapabilityGrid'
import HistoryStrip  from './components/HistoryStrip'
import { useGenerate } from './hooks/useGenerate'

export default function App() {
  const {
    phase, route, activeAgent, doneAgents,
    output, error, history, isBackendLive, liveText,
    submit, reset,
  } = useGenerate()

  const outputRef = useRef(null)
  const isIdle    = phase === 'idle'
  const isBusy    = phase === 'routing' || phase === 'running'

  // Scroll to output when it appears
  useEffect(() => {
    if ((phase === 'done' || liveText) && outputRef.current) {
      outputRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, [phase, !!liveText])

  function handleHistorySelect(input) {
    if (!isBusy) submit(input)
  }

  return (
    <div className="grid-bg min-h-screen flex flex-col" style={{ background: '#0D0D0D' }}>
      <Header isBackendLive={isBackendLive} agentCount={5} />

      <main className="relative z-10 flex-1 flex flex-col items-center px-6 py-16"
        style={{ maxWidth: '860px', margin: '0 auto', width: '100%' }}
      >

        {/* Hero — only on idle */}
        {isIdle && <Hero />}

        {/* Input box — always visible */}
        <InputBox
          onSubmit={submit}
          onFill={v => submit(v)}
          disabled={isBusy}
        />

        {/* Agent pipeline — hide once streaming text starts arriving */}
        {!liveText && (
          <AgentPipeline
            phase={phase}
            route={route}
            activeAgent={activeAgent}
            doneAgents={doneAgents}
          />
        )}

        {/* Error */}
        {phase === 'error' && error && (
          <div
            className="w-full mt-5 px-5 py-4 rounded-2xl text-sm font-sans animate-fadeUp"
            style={{
              background: 'rgba(239,68,68,0.08)',
              border: '1px solid rgba(239,68,68,0.2)',
              color: '#FCA5A5',
            }}
          >
            <strong>Something went wrong:</strong> {error}
            <button
              onClick={reset}
              className="ml-4 underline text-xs"
              style={{ color: '#FCA5A5' }}
            >
              Try again
            </button>
          </div>
        )}

        {/* Output / streaming area */}
        <div ref={outputRef} className="w-full">
          {/* Live streaming preview while tokens arrive */}
          {phase === 'running' && liveText && (
            <OutputCard
              output={{
                result:   liveText,
                label:    route?.label ?? 'Generating…',
                type:     route?.type  ?? 'stream',
                agents:   route?.agents ?? [],
              }}
              isStreaming={true}
              onReset={reset}
            />
          )}

          {/* Final completed document */}
          {phase === 'done' && output && (
            <OutputCard output={output} onReset={reset} />
          )}
        </div>

        {/* Recent history */}
        {isIdle && history.length > 0 && (
          <HistoryStrip history={history} onSelect={handleHistorySelect} />
        )}

        {/* Capability grid — only on idle screen */}
        {isIdle && (
          <CapabilityGrid onFill={submit} disabled={isBusy} />
        )}

      </main>
    </div>
  )
}
