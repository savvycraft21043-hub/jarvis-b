import React from 'react'

export function Card({ className = '', children }) {
  return <div className={`rounded-2xl border border-zinc-800 bg-zinc-900/80 p-4 shadow-panel ${className}`}>{children}</div>
}

export function Badge({ children }) {
  return <span className="rounded-full border border-zinc-700 bg-zinc-800 px-2 py-1 text-xs text-zinc-300">{children}</span>
}

export function SectionTitle({ title, subtitle }) {
  return (
    <div className="mb-4">
      <h2 className="text-lg font-semibold text-zinc-100">{title}</h2>
      <p className="text-sm text-zinc-400">{subtitle}</p>
    </div>
  )
}
