import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  Rocket, Monitor, Search, Target, TrendingUp, BarChart2,
  Video, BookOpen, Calendar, GraduationCap, Briefcase, FileText,
  ClipboardList, Users, FileCheck, Heart, Plane, ChefHat,
  Lightbulb, MessageCircle,
} from 'lucide-react'
import { CAPABILITY_GRID } from '../data'

const ICON_MAP = {
  Rocket, Monitor, Search, Target, TrendingUp, BarChart2,
  Video, BookOpen, Calendar, GraduationCap, Briefcase, FileText,
  ClipboardList, Users, FileCheck, Heart, Plane, ChefHat,
  Lightbulb, MessageCircle,
}

const GRID_CATEGORIES = [
  { key: 'all',         label: 'All' },
  { key: 'business',    label: 'Business' },
  { key: 'creators',    label: 'Creators' },
  { key: 'students',    label: 'Students' },
  { key: 'agencies',    label: 'Agencies' },
  { key: 'freelancers', label: 'Freelancers' },
  { key: 'personal',    label: 'Personal Life' },
  { key: 'general',     label: 'General' },
]

export default function CapabilityGrid({ onFill, disabled }) {
  const [activeCategory, setActiveCategory] = useState('all')

  const filtered = activeCategory === 'all'
    ? CAPABILITY_GRID
    : CAPABILITY_GRID.filter(item => item.category === activeCategory)

  return (
    <div className="w-full mt-14 animate-fadeUp" style={{ animationDelay: '0.4s' }}>

      {/* Section header */}
      <div className="mb-5">
        <span
          className="text-[11px] font-sans font-medium tracking-[1.5px] uppercase"
          style={{ color: '#6B6661' }}
        >
          What can Orion do?
        </span>
      </div>

      {/* Category filter tabs */}
      <div className="flex flex-wrap gap-1.5 mb-6">
        {GRID_CATEGORIES.map(cat => (
          <button
            key={cat.key}
            onClick={() => setActiveCategory(cat.key)}
            className="text-[11px] font-sans px-3 py-1.5 rounded-full transition-all duration-200"
            style={{
              border: '1px solid',
              borderColor: activeCategory === cat.key ? 'rgba(232,197,71,0.35)' : 'rgba(255,255,255,0.08)',
              background: activeCategory === cat.key ? 'rgba(232,197,71,0.10)' : 'transparent',
              color: activeCategory === cat.key ? '#E8C547' : '#6B6661',
            }}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Cards grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))',
          gap: '12px',
        }}
      >
        {filtered.map((item, index) => {
          const IconComponent = ICON_MAP[item.iconName]
          return (
            <motion.button
              key={item.title}
              initial={{ opacity: 0, y: 18 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.28, delay: index * 0.04, ease: 'easeOut' }}
              onClick={() => !disabled && onFill(item.prompt)}
              disabled={disabled}
              className="text-left transition-colors duration-200"
              style={{
                background: '#161616',
                border: '1px solid rgba(255,255,255,0.06)',
                borderRadius: '16px',
                padding: '18px',
                cursor: disabled ? 'not-allowed' : 'pointer',
                display: 'flex',
                flexDirection: 'column',
                gap: '10px',
              }}
              onMouseEnter={e => {
                if (!disabled) {
                  e.currentTarget.style.background = '#1C1C1C'
                  e.currentTarget.style.borderColor = 'rgba(255,255,255,0.12)'
                }
              }}
              onMouseLeave={e => {
                e.currentTarget.style.background = '#161616'
                e.currentTarget.style.borderColor = 'rgba(255,255,255,0.06)'
              }}
            >
              {/* Icon box */}
              <div
                style={{
                  width: '36px',
                  height: '36px',
                  borderRadius: '10px',
                  background: item.iconBg,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  flexShrink: 0,
                }}
              >
                {IconComponent && (
                  <IconComponent size={17} color={item.iconColor} strokeWidth={1.6} />
                )}
              </div>

              {/* Title + audience badge */}
              <div>
                <div
                  className="font-serif leading-snug mb-2"
                  style={{ color: '#F0EDE8', fontSize: '15px' }}
                >
                  {item.title}
                </div>
                <span
                  className="inline-block text-[10px] font-sans font-medium px-2 py-0.5 rounded-full"
                  style={{
                    background: item.iconBg,
                    color: item.iconColor,
                  }}
                >
                  {item.audience}
                </span>
              </div>

              {/* Description */}
              <p
                className="font-sans text-[12px] font-light leading-relaxed"
                style={{ color: '#6B6661' }}
              >
                {item.description}
              </p>

              {/* Divider */}
              <div style={{ height: '1px', background: 'rgba(255,255,255,0.06)' }} />

              {/* Outcome */}
              <div className="font-sans text-[11px]" style={{ color: '#4A4643' }}>
                Outcome:{' '}
                <span style={{ color: item.iconColor }}>{item.outcome}</span>
              </div>
            </motion.button>
          )
        })}
      </div>
    </div>
  )
}
