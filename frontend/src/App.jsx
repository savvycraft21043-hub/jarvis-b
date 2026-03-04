import { Route, Routes } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import CommandCenter from './pages/CommandCenter'
import OpportunityRadar from './pages/OpportunityRadar'
import SignalFeed from './pages/SignalFeed'
import GraphView from './pages/GraphView'
import CompanyPage from './pages/CompanyPage'

export default function App() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 bg-zinc-950 p-6">
        <Routes>
          <Route path="/" element={<CommandCenter />} />
          <Route path="/opportunities" element={<OpportunityRadar />} />
          <Route path="/signals" element={<SignalFeed />} />
          <Route path="/graph" element={<GraphView />} />
          <Route path="/companies/:id" element={<CompanyPage />} />
        </Routes>
      </main>
    </div>
  )
}
