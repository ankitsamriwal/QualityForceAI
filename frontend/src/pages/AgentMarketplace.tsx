import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { agentsApi, executionsApi, AgentMetadata, AgentInput } from '@/lib/api'
import { Play, CheckCircle2, Clock, Upload, AlertCircle, X, Loader2 } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export function AgentMarketplace() {
  const [selectedAgents, setSelectedAgents] = useState<Set<string>>(new Set())
  const [inputs, setInputs] = useState<Record<string, AgentInput>>({})
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null)
  const navigate = useNavigate()
  const queryClient = useQueryClient()

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
    onSuccess: (data) => {
      showToast('Tests started successfully! Redirecting to execution monitor...', 'success')
      setSelectedAgents(new Set())
      setInputs({})
      setErrors({})
      queryClient.invalidateQueries({ queryKey: ['executions'] })

      // Redirect to executions page after 2 seconds
      setTimeout(() => {
        navigate('/executions')
      }, 2000)
    },
    onError: (error: any) => {
      const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to start execution'
      showToast(`Error: ${errorMessage}`, 'error')
      console.error('Execution error:', error)
    },
  })

  const showToast = (message: string, type: 'success' | 'error') => {
    setToast({ message, type })
    setTimeout(() => setToast(null), 5000)
  }

  const validateInputs = (): boolean => {
    const newErrors: Record<string, string> = {}
    let hasErrors = false

    selectedAgents.forEach((agentType) => {
      const agent = agents?.find(a => a.agent_type === agentType)
      if (!agent) return

      const agentInputs = inputs[agentType] || {}

      // Check required inputs
      agent.required_inputs.forEach((requiredInput) => {
        const value = agentInputs[requiredInput as keyof AgentInput]

        if (!value) {
          newErrors[`${agentType}_${requiredInput}`] = `${requiredInput} is required`
          hasErrors = true
        } else if (typeof value === 'string' && value.trim() === '') {
          newErrors[`${agentType}_${requiredInput}`] = `${requiredInput} cannot be empty`
          hasErrors = true
        } else if (Array.isArray(value) && value.length === 0) {
          newErrors[`${agentType}_${requiredInput}`] = `${requiredInput} must have at least one item`
          hasErrors = true
        }
      })

      // Validate endpoints format
      if (agentInputs.endpoints && agentInputs.endpoints.length > 0) {
        const invalidEndpoints = agentInputs.endpoints.filter(ep => {
          return ep && !ep.startsWith('/') && !ep.startsWith('http')
        })
        if (invalidEndpoints.length > 0) {
          newErrors[`${agentType}_endpoints`] = 'Endpoints must start with / or http'
          hasErrors = true
        }
      }
    })

    setErrors(newErrors)
    return !hasErrors
  }

  const toggleAgent = (agentType: string) => {
    const newSelected = new Set(selectedAgents)
    if (newSelected.has(agentType)) {
      newSelected.delete(agentType)
      // Clear inputs and errors for deselected agent
      const newInputs = { ...inputs }
      delete newInputs[agentType]
      setInputs(newInputs)

      const newErrors = { ...errors }
      Object.keys(newErrors).forEach(key => {
        if (key.startsWith(agentType)) {
          delete newErrors[key]
        }
      })
      setErrors(newErrors)
    } else {
      newSelected.add(agentType)
    }
    setSelectedAgents(newSelected)
  }

  const handleExecute = () => {
    if (selectedAgents.size === 0) {
      showToast('Please select at least one agent', 'error')
      return
    }

    if (!validateInputs()) {
      showToast('Please fix validation errors before executing', 'error')
      return
    }

    executeMutation.mutate(Array.from(selectedAgents))
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        <span className="ml-2 text-gray-600">Loading agents...</span>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Toast Notification */}
      {toast && (
        <div className={`fixed top-4 right-4 z-50 max-w-md rounded-lg shadow-lg p-4 ${
          toast.type === 'success' ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
        }`}>
          <div className="flex items-start">
            <div className="flex-shrink-0">
              {toast.type === 'success' ? (
                <CheckCircle2 className="h-5 w-5 text-green-600" />
              ) : (
                <AlertCircle className="h-5 w-5 text-red-600" />
              )}
            </div>
            <div className="ml-3 flex-1">
              <p className={`text-sm font-medium ${
                toast.type === 'success' ? 'text-green-800' : 'text-red-800'
              }`}>
                {toast.message}
              </p>
            </div>
            <button
              onClick={() => setToast(null)}
              className="ml-4 flex-shrink-0 text-gray-400 hover:text-gray-600"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

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
          className="flex items-center px-6 py-3 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {executeMutation.isPending ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Starting...
            </>
          ) : (
            <>
              <Play className="mr-2 h-4 w-4" />
              Execute {selectedAgents.size > 0 && `(${selectedAgents.size})`}
            </>
          )}
        </button>
      </div>

      {/* Selected Agents Summary */}
      {selectedAgents.size > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-medium text-blue-900">
                {selectedAgents.size} agent{selectedAgents.size > 1 ? 's' : ''} selected
              </h3>
              <p className="text-xs text-blue-700 mt-1">
                Make sure to configure required inputs for each agent
              </p>
            </div>
            <button
              onClick={() => {
                setSelectedAgents(new Set())
                setInputs({})
                setErrors({})
              }}
              className="text-sm text-blue-600 hover:text-blue-700 font-medium"
            >
              Clear All
            </button>
          </div>
        </div>
      )}

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
            errors={errors}
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
  errors,
}: {
  agent: AgentMetadata
  isSelected: boolean
  onToggle: () => void
  inputs?: AgentInput
  onInputsChange: (inputs: AgentInput) => void
  errors: Record<string, string>
}) {
  const [showInputs, setShowInputs] = useState(false)

  const handleFileUpload = async (
    e: React.ChangeEvent<HTMLInputElement>,
    fieldName: string
  ) => {
    const file = e.target.files?.[0]
    if (!file) return

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert('File size must be less than 10MB')
      return
    }

    try {
      const text = await file.text()
      onInputsChange({
        ...inputs,
        [fieldName]: text,
      })
    } catch (error) {
      console.error('Error reading file:', error)
      alert('Failed to read file')
    }
  }

  const getErrorForField = (fieldName: string): string | undefined => {
    return errors[`${agent.agent_type}_${fieldName}`]
  }

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
            className={`ml-4 p-2 rounded-full transition-colors ${
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
                {/* Source Code Input */}
                {agent.required_inputs.includes('source_code') && (
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1">
                      Source Code {agent.required_inputs.includes('source_code') && <span className="text-red-500">*</span>}
                    </label>
                    <textarea
                      className={`w-full px-3 py-2 text-sm border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        getErrorForField('source_code') ? 'border-red-300' : 'border-gray-300'
                      }`}
                      rows={3}
                      placeholder="Paste source code or upload file..."
                      value={inputs?.source_code || ''}
                      onChange={(e) =>
                        onInputsChange({
                          ...inputs,
                          source_code: e.target.value,
                        })
                      }
                    />
                    <div className="mt-1 flex items-center justify-between">
                      <label className="cursor-pointer text-xs text-blue-600 hover:text-blue-700 flex items-center">
                        <Upload className="h-3 w-3 mr-1" />
                        Upload file
                        <input
                          type="file"
                          className="hidden"
                          accept=".py,.js,.ts,.java,.cpp,.c,.go,.rb,.php"
                          onChange={(e) => handleFileUpload(e, 'source_code')}
                        />
                      </label>
                      {getErrorForField('source_code') && (
                        <span className="text-xs text-red-600">{getErrorForField('source_code')}</span>
                      )}
                    </div>
                  </div>
                )}

                {/* Requirements Document Input */}
                {agent.required_inputs.includes('requirements_doc') && (
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1">
                      Requirements Document {agent.required_inputs.includes('requirements_doc') && <span className="text-red-500">*</span>}
                    </label>
                    <textarea
                      className={`w-full px-3 py-2 text-sm border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        getErrorForField('requirements_doc') ? 'border-red-300' : 'border-gray-300'
                      }`}
                      rows={3}
                      placeholder="Paste requirements or upload file..."
                      value={inputs?.requirements_doc || ''}
                      onChange={(e) =>
                        onInputsChange({
                          ...inputs,
                          requirements_doc: e.target.value,
                        })
                      }
                    />
                    <div className="mt-1 flex items-center justify-between">
                      <label className="cursor-pointer text-xs text-blue-600 hover:text-blue-700 flex items-center">
                        <Upload className="h-3 w-3 mr-1" />
                        Upload document
                        <input
                          type="file"
                          className="hidden"
                          accept=".txt,.md,.doc,.docx,.pdf"
                          onChange={(e) => handleFileUpload(e, 'requirements_doc')}
                        />
                      </label>
                      {getErrorForField('requirements_doc') && (
                        <span className="text-xs text-red-600">{getErrorForField('requirements_doc')}</span>
                      )}
                    </div>
                  </div>
                )}

                {/* Endpoints Input */}
                {agent.required_inputs.includes('endpoints') && (
                  <div>
                    <label className="block text-xs font-medium text-gray-700 mb-1">
                      Endpoints (comma-separated) {agent.required_inputs.includes('endpoints') && <span className="text-red-500">*</span>}
                    </label>
                    <input
                      type="text"
                      className={`w-full px-3 py-2 text-sm border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                        getErrorForField('endpoints') ? 'border-red-300' : 'border-gray-300'
                      }`}
                      placeholder="e.g., /api/users, https://api.example.com/products"
                      value={inputs?.endpoints?.join(', ') || ''}
                      onChange={(e) =>
                        onInputsChange({
                          ...inputs,
                          endpoints: e.target.value
                            .split(',')
                            .map((s) => s.trim())
                            .filter(s => s.length > 0),
                        })
                      }
                    />
                    {getErrorForField('endpoints') && (
                      <span className="text-xs text-red-600 mt-1 block">{getErrorForField('endpoints')}</span>
                    )}
                  </div>
                )}

                {/* FRD/BRD Inputs */}
                {(agent.optional_inputs.includes('frd') || agent.optional_inputs.includes('brd')) && (
                  <div className="space-y-2">
                    {agent.optional_inputs.includes('frd') && (
                      <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">
                          FRD (Functional Requirements)
                        </label>
                        <textarea
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md"
                          rows={2}
                          placeholder="Paste FRD or upload..."
                          value={inputs?.frd || ''}
                          onChange={(e) =>
                            onInputsChange({
                              ...inputs,
                              frd: e.target.value,
                            })
                          }
                        />
                        <label className="cursor-pointer text-xs text-blue-600 hover:text-blue-700 flex items-center mt-1">
                          <Upload className="h-3 w-3 mr-1" />
                          Upload FRD
                          <input
                            type="file"
                            className="hidden"
                            accept=".txt,.md,.doc,.docx,.pdf"
                            onChange={(e) => handleFileUpload(e, 'frd')}
                          />
                        </label>
                      </div>
                    )}

                    {agent.optional_inputs.includes('brd') && (
                      <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">
                          BRD (Business Requirements)
                        </label>
                        <textarea
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md"
                          rows={2}
                          placeholder="Paste BRD or upload..."
                          value={inputs?.brd || ''}
                          onChange={(e) =>
                            onInputsChange({
                              ...inputs,
                              brd: e.target.value,
                            })
                          }
                        />
                        <label className="cursor-pointer text-xs text-blue-600 hover:text-blue-700 flex items-center mt-1">
                          <Upload className="h-3 w-3 mr-1" />
                          Upload BRD
                          <input
                            type="file"
                            className="hidden"
                            accept=".txt,.md,.doc,.docx,.pdf"
                            onChange={(e) => handleFileUpload(e, 'brd')}
                          />
                        </label>
                      </div>
                    )}
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
