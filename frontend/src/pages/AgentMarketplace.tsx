import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { agentsApi, executionsApi, AgentMetadata, AgentInput } from '@/lib/api'
import { Play, CheckCircle2, Clock } from 'lucide-react'

export function AgentMarketplace() {
  const [selectedAgents, setSelectedAgents] = useState<Set<string>>(new Set())
  const [inputs, setInputs] = useState<Record<string, AgentInput>>({})

  const { data: agents, isLoading } = useQuery({
    queryKey: ['agents'],
    queryFn: () => agentsApi.list().then((res) => res.data),
  })

  const executeMutation = useMutation({
    mutationFn: async (agentTypes: string[]) => {
      const requests = agentTypes.map((type) => ({
        agent_type: type,
        inputs: inputs[type] || {},
      }))

      if (requests.length === 1) {
        return executionsApi.execute(requests[0])
      }
      return executionsApi.executeBatch(requests, true)
    },
    onSuccess: () => {
      alert('Execution started successfully!')
      setSelectedAgents(new Set())
    },
  })

  const toggleAgent = (agentType: string) => {
    const newSelected = new Set(selectedAgents)
    if (newSelected.has(agentType)) {
      newSelected.delete(agentType)
    } else {
      newSelected.add(agentType)
    }
    setSelectedAgents(newSelected)
  }

  const handleExecute = () => {
    if (selectedAgents.size === 0) {
      alert('Please select at least one agent')
      return
    }
    executeMutation.mutate(Array.from(selectedAgents))
  }

  if (isLoading) {
    return <div className="text-center py-12">Loading agents...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Agent Marketplace</h2>
          <p className="mt-2 text-sm text-gray-600">
            Select and configure testing agents to execute
          </p>
        </div>
        <button
          onClick={handleExecute}
          disabled={selectedAgents.size === 0 || executeMutation.isPending}
          className="flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Play className="mr-2 h-4 w-4" />
          Execute {selectedAgents.size > 0 && `(${selectedAgents.size})`}
        </button>
      </div>

      {/* Agent Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents?.map((agent) => (
          <AgentCard
            key={agent.agent_type}
            agent={agent}
            isSelected={selectedAgents.has(agent.agent_type)}
            onToggle={() => toggleAgent(agent.agent_type)}
            inputs={inputs[agent.agent_type]}
            onInputsChange={(newInputs) =>
              setInputs({ ...inputs, [agent.agent_type]: newInputs })
            }
          />
        ))}
      </div>
    </div>
  )
}

function AgentCard({
  agent,
  isSelected,
  onToggle,
  inputs,
  onInputsChange,
}: {
  agent: AgentMetadata
  isSelected: boolean
  onToggle: () => void
  inputs?: AgentInput
  onInputsChange: (inputs: AgentInput) => void
}) {
  const [showInputs, setShowInputs] = useState(false)

  return (
    <div
      className={`bg-white rounded-lg shadow-md overflow-hidden transition-all ${
        isSelected ? 'ring-2 ring-blue-500' : ''
      }`}
    >
      <div className="p-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900">
              {agent.name}
            </h3>
            <p className="mt-1 text-sm text-gray-500">{agent.description}</p>
          </div>
          <button
            onClick={onToggle}
            className={`ml-4 p-2 rounded-full ${
              isSelected
                ? 'bg-blue-100 text-blue-600'
                : 'bg-gray-100 text-gray-400 hover:bg-gray-200'
            }`}
          >
            <CheckCircle2 className="h-5 w-5" />
          </button>
        </div>

        <div className="mt-4 space-y-2">
          <div className="flex items-center text-sm text-gray-500">
            <Clock className="h-4 w-4 mr-2" />
            ~{Math.floor(agent.estimated_duration / 60)} min
          </div>

          <div className="flex flex-wrap gap-1 mt-2">
            {agent.capabilities.slice(0, 3).map((cap) => (
              <span
                key={cap}
                className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-blue-100 text-blue-800"
              >
                {cap}
              </span>
            ))}
            {agent.capabilities.length > 3 && (
              <span className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-600">
                +{agent.capabilities.length - 3} more
              </span>
            )}
          </div>
        </div>

        {isSelected && (
          <div className="mt-4">
            <button
              onClick={() => setShowInputs(!showInputs)}
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              {showInputs ? 'Hide' : 'Configure'} Inputs
            </button>

            {showInputs && (
              <div className="mt-3 space-y-3">
                {agent.required_inputs.includes('source_code') && (
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1">
                      Source Code
                    </label>
                    <textarea
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md"
                      rows={3}
                      placeholder="Paste source code..."
                      value={inputs?.source_code || ''}
                      onChange={(e) =>
                        onInputsChange({
                          ...inputs,
                          source_code: e.target.value,
                        })
                      }
                    />
                  </div>
                )}

                {agent.required_inputs.includes('requirements_doc') && (
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1">
                      Requirements Document
                    </label>
                    <textarea
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md"
                      rows={3}
                      placeholder="Paste requirements..."
                      value={inputs?.requirements_doc || ''}
                      onChange={(e) =>
                        onInputsChange({
                          ...inputs,
                          requirements_doc: e.target.value,
                        })
                      }
                    />
                  </div>
                )}

                {agent.required_inputs.includes('endpoints') && (
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1">
                      Endpoints (comma-separated)
                    </label>
                    <input
                      type="text"
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md"
                      placeholder="/api/users, /api/products"
                      value={inputs?.endpoints?.join(', ') || ''}
                      onChange={(e) =>
                        onInputsChange({
                          ...inputs,
                          endpoints: e.target.value
                            .split(',')
                            .map((s) => s.trim()),
                        })
                      }
                    />
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
