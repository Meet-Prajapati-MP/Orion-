import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Copy, Download, Check, FileText, RotateCcw, Printer } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export default function OutputCard({ output, onReset, isStreaming = false }) {
  const [copied, setCopied] = useState(false)

  if (!output) return null

  async function handleCopy() {
    await navigator.clipboard.writeText(output.result)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  function handleDownload() {
    const blob = new Blob([output.result], { type: 'text/markdown' })
    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
    a.download = `orion-${output.type}-${Date.now()}.md`
    a.click()
    URL.revokeObjectURL(a.href)
  }

  // Opens a styled print window → user clicks "Save as PDF" in the print dialog
  function handlePrintPDF() {
    const markdownEl = document.querySelector('.markdown-body')
    const htmlContent = markdownEl?.innerHTML ?? ''
    const win = window.open('', '_blank')
    if (!win) return
    win.document.write(`<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>${output.label ?? 'Orion Document'}</title>
  <style>
    body{font-family:Georgia,serif;max-width:800px;margin:40px auto;padding:20px;color:#1a1a1a;line-height:1.75}
    h1{font-size:26px;border-bottom:2px solid #222;padding-bottom:8px;margin-bottom:16px}
    h2{font-size:20px;margin-top:28px;color:#222}
    h3{font-size:15px;font-weight:600;margin-top:20px}
    p{margin-bottom:12px}
    ul,ol{padding-left:24px;margin-bottom:12px}
    li{margin-bottom:4px}
    table{width:100%;border-collapse:collapse;margin:16px 0;font-size:13px}
    th,td{border:1px solid #ddd;padding:8px 12px;text-align:left}
    th{background:#f5f5f5;font-weight:600}
    code{background:#f0f0f0;padding:2px 5px;border-radius:3px;font-family:monospace;font-size:12px}
    pre{background:#f5f5f5;padding:14px;border-radius:6px;overflow-x:auto;margin-bottom:14px}
    hr{border:1px solid #eee;margin:20px 0}
    blockquote{border-left:3px solid #ccc;padding-left:14px;color:#666;font-style:italic;margin:12px 0}
    strong{font-weight:600}
  </style>
</head>
<body>${htmlContent}</body>
</html>`)
    win.document.close()
    setTimeout(() => { win.print(); win.close() }, 400)
  }

  return (
    <motion.div
      className="w-full mt-7"
      initial={{ opacity: 0, y: 22, scale: 0.98 }}
      animate={{ opacity: 1, y: 0,  scale: 1    }}
      transition={{ duration: 0.45, ease: 'easeOut' }}
    >
      <div className="rounded-[20px] overflow-hidden" style={{ background: '#161616', border: '1px solid rgba(255,255,255,0.08)' }}>

        {/* Top bar */}
        <div
          className="flex items-center justify-between px-5 py-4"
          style={{ background: '#1E1E1E', borderBottom: '1px solid rgba(255,255,255,0.08)' }}
        >
          {/* Badge — shows "Generating…" with pulse during streaming */}
          {isStreaming ? (
            <div className="flex items-center gap-2 text-xs font-sans font-medium">
              <span
                className="w-1.5 h-1.5 rounded-full animate-breathe"
                style={{ background: '#E8C547', display: 'inline-block' }}
              />
              <span style={{ color: '#E8C547' }}>
                Generating {output.label}…
              </span>
            </div>
          ) : (
            <div
              className="flex items-center gap-2 text-xs font-sans font-medium px-3 py-1.5 rounded-full"
              style={{ background: 'rgba(232,197,71,0.12)', border: '1px solid rgba(232,197,71,0.22)', color: '#E8C547' }}
            >
              <FileText size={12} strokeWidth={1.8} />
              {output.label}
            </div>
          )}

          {/* Action buttons — hidden while streaming */}
          {!isStreaming && (
            <div className="flex gap-2">
              <ActionBtn icon={copied ? <Check size={12}/> : <Copy size={12}/>}  label={copied ? 'Copied!' : 'Copy'}    onClick={handleCopy}     />
              <ActionBtn icon={<Download size={12}/>}  label="Save .md"  onClick={handleDownload}  />
              <ActionBtn icon={<Printer size={12}/>}   label="Print PDF" onClick={handlePrintPDF}  />
            </div>
          )}
        </div>

        {/* Document content */}
        <div
          className="px-7 py-7 markdown-body overflow-y-auto"
          style={{ maxHeight: isStreaming ? '420px' : '480px' }}
        >
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {/* Append blinking cursor while streaming */}
            {isStreaming ? output.result + ' ▌' : output.result}
          </ReactMarkdown>
        </div>
      </div>

      {/* New document button — only when fully done */}
      <AnimatePresence>
        {!isStreaming && (
          <motion.button
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3, delay: 0.2 }}
            onClick={onReset}
            className="flex items-center justify-center gap-2 w-full mt-4 py-3 text-sm font-sans rounded-xl transition-all duration-200"
            style={{ background: 'none', border: '1px dashed rgba(255,255,255,0.1)', color: '#6B6661' }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.22)'; e.currentTarget.style.color = '#F0EDE8'; e.currentTarget.style.background = '#1E1E1E' }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.1)';  e.currentTarget.style.color = '#6B6661';  e.currentTarget.style.background = 'none' }}
          >
            <RotateCcw size={14} />
            Start a new document
          </motion.button>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

function ActionBtn({ icon, label, onClick }) {
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-1.5 text-xs font-sans px-3 py-1.5 rounded-lg transition-all duration-200"
      style={{ background: 'none', border: '1px solid rgba(255,255,255,0.08)', color: '#6B6661' }}
      onMouseEnter={e => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.2)'; e.currentTarget.style.color = '#F0EDE8' }}
      onMouseLeave={e => { e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)'; e.currentTarget.style.color = '#6B6661' }}
    >
      {icon}
      {label}
    </button>
  )
}
