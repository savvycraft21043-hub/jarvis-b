import { Link, useLocation } from 'react-router-dom'

const nav = [
  ['/', 'Command Center'],
  ['/opportunities', 'Opportunity Radar'],
  ['/signals', 'Signal Feed'],
  ['/graph', 'Graph View'],
]

export default function Sidebar() {
  const { pathname } = useLocation()
  return (
    <aside className="w-64 border-r border-zinc-800 bg-zinc-950 p-4">
      <h1 className="mb-6 text-xl font-bold tracking-tight">JARVIS</h1>
      <nav className="space-y-2">
        {nav.map(([path, label]) => (
          <Link
            key={path}
            to={path}
            className={`block rounded-xl px-3 py-2 text-sm transition ${
              pathname === path ? 'bg-zinc-800 text-zinc-100' : 'text-zinc-400 hover:bg-zinc-900 hover:text-zinc-100'
            }`}
          >
            {label}
          </Link>
        ))}
      </nav>
    </aside>
  )
}
