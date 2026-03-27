import { useRef, useEffect, useState } from 'react'
import { Send } from 'lucide-react'
import { QUICK_PROMPTS, CATEGORY_FILTERS } from '../data'

export default function InputBox({ onSubmit, disabled }) {
  const [value, setValue]       = useState('')
  const [activecat, setActiveCat] = useState('all')
  const textareaRef             = useRef(null)

  // Auto-resize textarea
  useEffect(() => {
    const ta = textareaRef.current
    if (!ta) return
    ta.style.height = 'auto'
    ta.style.height = Math.min(ta.scrollHeight, 180) + 'px'
  }, [value])

  // Focus on mount
  useEffect(() => { textareaRef.current?.focus() }, [])

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  function handleSend() {
    const trimmed = value.trim()
    if (!trimmed || disabled) return
    onSubmit(trimmed)
    setValue('')
  }

  function fillInput(text) {
    setValue(text)
    textareaRef.current?.focus()
  }

  function handleCatClick(cat) {
    setActiveCat(cat.key)
    if (cat.prompt) fillInput(cat.prompt)
  }

  return (
    <div className="w-full animate-fadeUp" style={{ animationDelay: '0.15s' }}>
      {/* Main input card */}
      <div
        className="relative rounded-[20px] transition-all duration-300"
        style={{
          background: '#161616',
          border: '1px solid rgba(255,255,255,0.08)',
          padding: '20px 20px 16px 24px',
        }}
        onFocus={() => {}}
      >
        <style>{`
          .input-focused { border-color: rgba(232,197,71,0.32) !important; box-shadow: 0 0 0 4px rgba(232,197,71,0.06), 0 0 40px rgba(232,197,71,0.04) !important; }
        `}</style>

        <div
          className="rounded-[20px] transition-all duration-300"
          style={{ border: '1px solid rgba(255,255,255,0.08)', padding: '20px 20px 16px 24px', background: '#161616', margin: '-20px -20px -16px -24px' }}
          onFocus={e => e.currentTarget.style.cssText += ';border-color:rgba(232,197,71,0.32);box-shadow:0 0 0 4px rgba(232,197,71,0.06)'}
          onBlur={e => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)'; e.currentTarget.style.boxShadow = '' }}
        >
          <div className="flex items-end gap-3">
            <textarea
              ref={textareaRef}
              value={value}
              onChange={e => setValue(e.target.value)}
              onKeyDown={handleKey}
              placeholder="e.g. I want to start a sustainable fashion brand targeting Gen Z in India…"
              rows={1}
              maxLength={1000}
              disabled={disabled}
              className="flex-1 font-sans text-base font-light resize-none outline-none border-none"
              style={{
                background: 'transparent',
                color: '#F0EDE8',
                caretColor: '#E8C547',
                minHeight: '28px',
                maxHeight: '180px',
                overflow: 'auto',
                lineHeight: '1.6',
              }}
            />
            <button
              onClick={handleSend}
              disabled={disabled || !value.trim()}
              className="w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0 transition-all duration-200"
              style={{
                background: '#E8C547',
                color: '#0D0D0D',
                opacity: disabled || !value.trim() ? 0.4 : 1,
                cursor: disabled || !value.trim() ? 'not-allowed' : 'pointer',
              }}
              onMouseEnter={e => { if (!disabled && value.trim()) e.currentTarget.style.background = '#f0d060' }}
              onMouseLeave={e => { e.currentTarget.style.background = '#E8C547' }}
            >
              <Send size={17} strokeWidth={2.2} />
            </button>
          </div>

          {/* Bottom bar */}
          <div className="flex items-center justify-between mt-3 pt-3" style={{ borderTop: '1px solid rgba(255,255,255,0.08)' }}>
            <span className="text-xs font-sans" style={{ color: '#6B6661' }}>
              Shift+Enter for new line · Enter to send
            </span>
            <span className="text-xs font-sans font-light tabular-nums" style={{ color: '#4A4643' }}>
              {value.length} / 1000
            </span>
          </div>
        </div>
      </div>

      {/* Quick prompts */}
      <div className="flex flex-wrap gap-2 justify-center mt-6 animate-fadeUp" style={{ animationDelay: '0.25s' }}>
        {QUICK_PROMPTS.map((q) => (
          <button
            key={q.label}
            onClick={() => fillInput(q.prompt)}
            disabled={disabled}
            className="flex items-center gap-1.5 text-xs font-sans px-3.5 py-1.5 rounded-full transition-all duration-200"
            style={{
              background: '#161616',
              border: '1px solid rgba(255,255,255,0.08)',
              color: '#6B6661',
            }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.2)'; e.currentTarget.style.color = '#F0EDE8' }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)'; e.currentTarget.style.color = '#6B6661' }}
          >
            <span style={{ fontSize: '13px' }}>{q.icon}</span>
            {q.label}
          </button>
        ))}
      </div>

      {/* Category filter */}
      <div className="flex flex-wrap gap-1.5 justify-center mt-4 animate-fadeUp" style={{ animationDelay: '0.35s' }}>
        {CATEGORY_FILTERS.map((cat) => (
          <button
            key={cat.key}
            onClick={() => handleCatClick(cat)}
            disabled={disabled}
            className="text-[11px] font-sans px-2.5 py-1 rounded-full transition-all duration-200"
            style={{
              border: '1px solid',
              borderColor: activecat === cat.key ? 'rgba(232,197,71,0.25)' : 'rgba(255,255,255,0.08)',
              background: activecat === cat.key ? 'rgba(232,197,71,0.12)' : 'transparent',
              color: activecat === cat.key ? '#E8C547' : '#4A4643',
            }}
          >
            {cat.label}
          </button>
        ))}
      </div>
    </div>
  )
}
