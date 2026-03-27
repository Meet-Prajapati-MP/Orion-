import { Zap } from 'lucide-react'

export default function Header({ isBackendLive, agentCount = 5 }) {
  return (
    <header className="relative z-10 flex items-center justify-between px-10 py-5 border-b border-white/[0.08]">
      {/* Logo */}
      <div className="flex items-center gap-3">
        <span className="font-serif text-xl text-ink tracking-tight">Orion</span>
        <span className="text-[10px] font-sans font-medium tracking-[2px] uppercase px-2 py-0.5 rounded-full border"
          style={{ background: 'rgba(232,197,71,0.12)', borderColor: 'rgba(232,197,71,0.22)', color: '#E8C547' }}>
          Multi-Agent
        </span>
      </div>

      {/* Status */}
      <div className="flex items-center gap-2">
        <span
          className="w-1.5 h-1.5 rounded-full animate-breathe"
          style={{ background: isBackendLive ? '#4ADE80' : '#E8C547' }}
        />
        <span className="text-xs text-muted font-sans">
          {isBackendLive ? `${agentCount} agents live` : `${agentCount} agents ready`}
        </span>
      </div>
    </header>
  )
}
