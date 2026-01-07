import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { executionsApi } from '@/lib/api'
import { useNavigate } from 'react-router-dom'
import {
  Play,
  Square,
  CheckCircle2,
  XCircle,
  Clock,
  Eye,
  Loader2,
} from 'lucide-react'

export function ExecutionMonitor() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { data: executions, isLoading } = useQuery({
    queryKey: ['executions'],
    queryFn: () => executionsApi.list().then((res) => res.data),
    refetchInterval: 3000,
  })

  const cancelMutation = useMutation({
    mutationFn: (executionId: string) => executionsApi.cancel(executionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['executions'] })
    },
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Execution Monitor</h2>
        <p className="mt-2 text-sm text-gray-600">
          Track and manage test executions in real-time
        </p>
      </div>

      {/* Active Executions */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">
            Active Executions
          </h3>
        </div>
        <div className="divide-y divide-gray-200">
          {executions
            ?.filter((e) => e.status === 'running')
            .map((execution) => (
              <ExecutionRow
                key={execution.execution_id}
                execution={execution}
                onCancel={() => cancelMutation.mutate(execution.execution_id)}
                onView={() => navigate(`/results/${execution.execution_id}`)}
              />
            ))}
          {executions?.filter((e) => e.status === 'running').length === 0 && (
            <div className="px-6 py-12 text-center text-gray-500">
              No active executions
            </div>
          )}
        </div>
      </div>

      {/* Completed Executions */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">
            Recent Executions
          </h3>
        </div>
        <div className="divide-y divide-gray-200">
          {executions
            ?.filter((e) => e.status !== 'running')
            .slice(0, 10)
            .map((execution) => (
              <ExecutionRow
                key={execution.execution_id}
                execution={execution}
                onView={() => navigate(`/results/${execution.execution_id}`)}
              />
            ))}
        </div>
      </div>
    </div>
  )
}

function ExecutionRow({
  execution,
  onCancel,
  onView,
}: {
  execution: any
  onCancel?: () => void
  onView: () => void
}) {
  const statusIcons = {
    pending: Clock,
    running: Loader2,
    completed: CheckCircle2,
    failed: XCircle,
    cancelled: Square,
  }

  const StatusIcon = statusIcons[execution.status] || Clock

  const statusColors = {
    pending: 'text-gray-500',
    running: 'text-yellow-500',
    completed: 'text-green-500',
    failed: 'text-red-500',
    cancelled: 'text-gray-500',
  }

  return (
    <div className="px-6 py-4 hover:bg-gray-50">
      <div className="flex items-center justify-between">
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-3">
            <StatusIcon
              className={`h-5 w-5 ${statusColors[execution.status]} ${
                execution.status === 'running' ? 'animate-spin' : ''
              }`}
            />
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-sm font-medium text-gray-900">
                  {execution.agent_type}
                </span>
                <StatusBadge status={execution.status} />
              </div>
              <div className="text-sm text-gray-500">
                Started: {new Date(execution.start_time).toLocaleString()}
              </div>
              {execution.duration && (
                <div className="text-sm text-gray-500">
                  Duration: {execution.duration.toFixed(2)}s
                </div>
              )}
            </div>
          </div>
        </div>

        {execution.status !== 'running' && (
          <div className="flex items-center space-x-4">
            <div className="text-sm text-gray-500">
              {execution.total_tests} tests
            </div>
            {execution.total_tests > 0 && (
              <div className="flex items-center space-x-2">
                <span className="text-sm text-green-600">
                  {execution.passed_tests} passed
                </span>
                <span className="text-sm text-red-600">
                  {execution.failed_tests} failed
                </span>
              </div>
            )}
          </div>
        )}

        <div className="flex items-center space-x-2 ml-4">
          {execution.status === 'running' && onCancel && (
            <button
              onClick={onCancel}
              className="p-2 text-red-600 hover:bg-red-50 rounded-md"
            >
              <Square className="h-4 w-4" />
            </button>
          )}
          <button
            onClick={onView}
            className="p-2 text-blue-600 hover:bg-blue-50 rounded-md"
          >
            <Eye className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  )
}

function StatusBadge({ status }: { status: string }) {
  const statusClasses = {
    pending: 'bg-gray-100 text-gray-800',
    running: 'bg-yellow-100 text-yellow-800',
    completed: 'bg-green-100 text-green-800',
    failed: 'bg-red-100 text-red-800',
    cancelled: 'bg-gray-100 text-gray-800',
  }

  return (
    <span
      className={`px-2 py-0.5 text-xs font-medium rounded-full ${
        statusClasses[status] || statusClasses.pending
      }`}
    >
      {status}
    </span>
  )
}
