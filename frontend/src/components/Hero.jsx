export default function Hero() {
  return (
    <div className="text-center mb-14 animate-fadeUp">
      {/* Eyebrow */}
      <div className="flex items-center justify-center gap-3 mb-5">
        <span className="block w-8 h-px" style={{ background: 'linear-gradient(90deg,transparent,#E8C547)' }} />
        <span className="text-[11px] font-sans font-medium tracking-[2.5px] uppercase" style={{ color: '#E8C547' }}>
          One input. Any document.
        </span>
        <span className="block w-8 h-px" style={{ background: 'linear-gradient(90deg,#E8C547,transparent)' }} />
      </div>

      {/* Heading */}
      <h1 className="font-serif text-[58px] leading-[1.08] tracking-[-2px] text-ink mb-5">
        Tell me what<br />you{' '}
        <em className="not-italic font-serif" style={{ color: '#E8C547' }}>need</em>{' '}to build
      </h1>

      {/* Sub */}
      <p className="font-sans text-base leading-relaxed max-w-[440px] mx-auto font-light" style={{ color: '#6B6661' }}>
        Describe your goal in plain language. The right team of AI agents assembles automatically.
      </p>
    </div>
  )
}
