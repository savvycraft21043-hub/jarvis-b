import { useEffect, useState } from 'react'
import { fetchOpportunities } from '../lib/api'
import { Badge, Card, SectionTitle } from '../components/ui'

export default function OpportunityRadar() {
  const [data, setData] = useState([])

  useEffect(() => {
    fetchOpportunities().then(setData)
  }, [])

  return (
    <div>
      <SectionTitle title="Opportunity Radar" subtitle="High-signal business opportunities detected by agents." />
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {data.map((o) => (
          <Card key={o.id} className="space-y-3">
            <div className="flex justify-between">
              <Badge>{o.industry}</Badge>
              <Badge>{Math.round(o.opportunity_score * 100)}</Badge>
            </div>
            <h3 className="font-semibold">{o.problem}</h3>
            <p className="text-sm text-zinc-400">{o.summary}</p>
            <p className="text-xs text-zinc-500">{o.company_name}</p>
          </Card>
        ))}
      </div>
    </div>
  )
}
