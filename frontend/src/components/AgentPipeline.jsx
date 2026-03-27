import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

export default function AgentPipeline({ phase, route, activeAgent, doneAgents }) {
  const [showType, setShowType] = useState(false)

  useEffect(() => {
    if (phase === 'running') {
      const t = setTimeout(() => setShowType(true), 400)
      return () => clearTimeout(t)
    }
    setShowType(false)
  }, [phase])

  const visible = phase === 'routing' || phase === 'running'

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.3, ease: 'easeOut' }}
          className="w-full rounded-[16px] mt-5"
          style={{ background: '#161616', border: '1px solid rgba(255,255,255,0.08)', padding: '18px 20px' }}
        >
          {/* Label row */}
          <div className="flex items-center gap-2 mb-4">
            {phase === 'routing' ? (
              <>
                <div
                  className="w-3 h-3 rounded-full border-[1.5px] animate-spin"
                  style={{ borderColor: 'rgba(255,255,255,0.15)', borderTopColor: '#E8C547' }}
                />
                <span className="text-[11px] font-sans font-medium tracking-[1.5px] uppercase" style={{ color: '#6B6661' }}>
                  Analysing your request…
                </span>
              </>
            ) : (
              <span className="text-[11px] font-sans font-medium tracking-[1.5px] uppercase" style={{ color: '#6B6661' }}>
                Agent pipeline running
              </span>
            )}
          </div>

          {/* Detected doc type */}
          <AnimatePresence>
            {showType && route && (
              <motion.div
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className="mb-4"
              >
                <div className="font-serif text-[22px] text-ink mb-0.5">{route.label}</div>
                <div className="text-[13px] font-sans font-light" style={{ color: '#6B6661' }}>
                  {route.agents.length}-agent pipeline · Audience: {route.audience}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Agent nodes */}
          {route && (
            <div className="flex flex-wrap items-center gap-1.5">
              {route.agents.map((agent, i) => {
                const isDone   = doneAgents.includes(i)
                const isActive = activeAgent === i && !isDone

                return (
                  <motion.div
                    key={agent}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.12, duration: 0.3 }}
                    className="flex items-center gap-1.5"
                  >
                    {i > 0 && (
                      <span
                        className="text-sm transition-opacity duration-500"
                        style={{ color: isDone || i <= activeAgent ? '#4A4643' : 'transparent', opacity: i <= (activeAgent ?? -1) || doneAgents.includes(i - 1) ? 1 : 0 }}
                      >
                        →
                      </span>
                    )}
                    <div
                      className="flex items-center gap-1.5 text-xs font-sans px-3 py-1.5 rounded-full transition-all duration-500"
                      style={{
                        border: '1px solid',
                        borderColor: isDone ? 'rgba(74,222,128,0.3)' : isActive ? 'rgba(232,197,71,0.3)' : 'rgba(255,255,255,0.08)',
                        background:  isDone ? 'rgba(74,222,128,0.1)'  : isActive ? 'rgba(232,197,71,0.12)' : 'transparent',
                        color:       isDone ? '#4ADE80'                : isActive ? '#E8C547'               : '#4A4643',
                        opacity:     i <= Math.max(activeAgent ?? -1, doneAgents.length - 1) ? 1 : 0.3,
                        transform:   i <= Math.max(activeAgent ?? -1, doneAgents.length - 1) ? 'translateX(0)' : 'translateX(-6px)',
                      }}
                    >
                      <span className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: 'currentColor' }} />
                      {agent}
                      {isDone && <span style={{ fontSize: '9px', marginLeft: '2px' }}>✓</span>}
                      {isActive && (
                        <span
                          className="w-2.5 h-2.5 rounded-full border-[1.5px] animate-spin flex-shrink-0"
                          style={{ borderColor: 'rgba(232,197,71,0.3)', borderTopColor: '#E8C547' }}
                        />
                      )}
                    </div>
                  </motion.div>
                )
              })}
            </div>
          )}
        </motion.div>
      )}
    </AnimatePresence>
  )
}
