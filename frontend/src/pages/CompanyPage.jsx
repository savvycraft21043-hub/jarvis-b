import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchCompany } from '../lib/api'
import { Badge, Card, SectionTitle } from '../components/ui'

export default function CompanyPage() {
  const { id } = useParams()
  const [company, setCompany] = useState(null)

  useEffect(() => {
    fetchCompany(id).then(setCompany)
  }, [id])

  if (!company) return <p className="text-zinc-400">Loading company intelligence...</p>

  return (
    <div className="space-y-4">
      <SectionTitle title={company.name} subtitle="Company Intelligence" />
      <Card>
        <div className="mb-3 flex gap-2">
          {company.tools.map((t) => <Badge key={t}>{t}</Badge>)}
        </div>
        <p className="text-sm text-zinc-400">Opportunity Score: {Math.round(company.opportunity_score * 100)}</p>
      </Card>
      <Card>
        <h3 className="mb-2 font-semibold">Signals Timeline</h3>
        <div className="space-y-2 text-sm">
          {company.signals.map((s) => <p key={s.id}>{s.signal_time}: {s.problem}</p>)}
        </div>
      </Card>
    </div>
  )
}
