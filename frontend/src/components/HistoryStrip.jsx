export default function HistoryStrip({ history, onSelect }) {
  if (!history || history.length === 0) return null

  return (
    <div className="w-full mt-8 animate-fadeUp">
      <div
        className="text-[11px] font-sans font-medium tracking-[1.5px] uppercase mb-3"
        style={{ color: '#4A4643' }}
      >
        Recent
      </div>
      <div className="flex flex-wrap gap-2">
        {history.map((h) => (
          <button
            key={h.id}
            onClick={() => onSelect(h.input)}
            className="flex items-center gap-2 text-xs font-sans px-3 py-1.5 rounded-lg transition-all duration-200 max-w-[240px] overflow-hidden"
            style={{
              background: '#161616',
              border: '1px solid rgba(255,255,255,0.08)',
              color: '#6B6661',
            }}
            onMouseEnter={e => {
              e.currentTarget.style.borderColor = 'rgba(255,255,255,0.2)'
              e.currentTarget.style.color = '#F0EDE8'
            }}
            onMouseLeave={e => {
              e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)'
              e.currentTarget.style.color = '#6B6661'
            }}
          >
            <span
              className="text-[10px] font-medium px-1.5 py-0.5 rounded flex-shrink-0"
              style={{ background: 'rgba(232,197,71,0.12)', color: '#E8C547' }}
            >
              {h.label}
            </span>
            <span className="truncate">{h.input}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
