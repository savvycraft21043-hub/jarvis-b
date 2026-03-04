import { useEffect, useState } from 'react'
import { fetchCompanies, runPipeline, search } from '../lib/api'
import { Badge, Card, SectionTitle } from '../components/ui'

export default function CommandCenter() {
  const [query, setQuery] = useState('Find salons London')
  const [result, setResult] = useState(null)
  const [companies, setCompanies] = useState([])

  useEffect(() => {
    runPipeline().then(() => fetchCompanies().then(setCompanies))
  }, [])

  const onSearch = async (e) => {
    e.preventDefault()
    const data = await search(query)
    setResult(data)
  }

  return (
    <div className="space-y-6">
      <SectionTitle title="Command Center" subtitle="Ask JARVIS in natural language." />
      <Card>
        <form onSubmit={onSearch} className="flex gap-2">
          <input
            className="w-full rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-3 text-sm outline-none focus:border-blue-500"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Find Shopify merchants reporting inventory failures"
          />
          <button className="rounded-xl bg-blue-600 px-4 py-3 text-sm font-medium hover:bg-blue-500">Search</button>
        </form>
      </Card>

      {result && (
        <Card>
          <h3 className="mb-3 font-semibold">Search Results</h3>
          <div className="grid gap-4 md:grid-cols-3">
            <ResultColumn title="Companies" items={result.companies} />
            <ResultColumn title="Signals" items={result.signals} />
            <ResultColumn title="Opportunities" items={result.opportunities} />
          </div>
        </Card>
      )}

      <Card>
        <h3 className="mb-3 font-semibold">Tracked Companies</h3>
        <div className="grid gap-3 md:grid-cols-2">
          {companies.map((c) => (
            <div key={c.id} className="rounded-xl border border-zinc-800 p-3">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">{c.name}</p>
                  <p className="text-sm text-zinc-400">{c.industry} · {c.location}</p>
                </div>
                <Badge>Score {Math.round(c.opportunity_score * 100)}</Badge>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}

function ResultColumn({ title, items }) {
  return (
    <div>
      <h4 className="mb-2 text-sm font-semibold text-zinc-300">{title}</h4>
      <div className="space-y-2">
        {items.length === 0 && <p className="text-xs text-zinc-500">No results</p>}
        {items.map((item) => (
          <div key={`${title}-${item.id}`} className="rounded-lg border border-zinc-800 p-2 text-xs text-zinc-300">
            {Object.entries(item).map(([k, v]) => (
              <div key={k}><span className="text-zinc-500">{k}:</span> {String(v)}</div>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}
