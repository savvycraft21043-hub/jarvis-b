import { useEffect, useState } from 'react'
import { fetchSignals } from '../lib/api'
import { Badge, Card, SectionTitle } from '../components/ui'

export default function SignalFeed() {
  const [signals, setSignals] = useState([])

  useEffect(() => {
    fetchSignals().then(setSignals)
  }, [])

  return (
    <div>
      <SectionTitle title="Signal Feed" subtitle="Live stream of discovered internet signals." />
      <div className="space-y-3">
        {signals.map((s) => (
          <Card key={s.id} className="flex items-start justify-between">
            <div>
              <p className="font-medium">{s.problem}</p>
              <p className="text-sm text-zinc-400">{s.company_name} · {s.source}</p>
            </div>
            <Badge>{Math.round(s.intent_score * 100)} intent</Badge>
          </Card>
        ))}
      </div>
    </div>
  )
}
