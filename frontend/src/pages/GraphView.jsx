import { useEffect, useState } from 'react'
import ForceGraph2D from 'react-force-graph-2d'
import { fetchGraph } from '../lib/api'
import { Card, SectionTitle } from '../components/ui'

export default function GraphView() {
  const [graph, setGraph] = useState({ nodes: [], edges: [] })

  useEffect(() => {
    fetchGraph().then((data) => setGraph({ nodes: data.nodes, links: data.edges }))
  }, [])

  return (
    <div>
      <SectionTitle title="Graph View" subtitle="Relationships between companies, tools, and opportunities." />
      <Card className="h-[560px]">
        <ForceGraph2D
          graphData={graph}
          nodeLabel="label"
          linkSource="source"
          linkTarget="target"
          backgroundColor="#09090b"
          nodeAutoColorBy="group"
        />
      </Card>
    </div>
  )
}
