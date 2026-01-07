import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from './components/Layout'
import { Dashboard } from './pages/Dashboard'
import { AgentMarketplace } from './pages/AgentMarketplace'
import { ExecutionMonitor } from './pages/ExecutionMonitor'
import { ResultsViewer } from './pages/ResultsViewer'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="marketplace" element={<AgentMarketplace />} />
          <Route path="executions" element={<ExecutionMonitor />} />
          <Route path="results/:executionId?" element={<ResultsViewer />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
