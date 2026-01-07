import { useQuery } from '@tanstack/react-query'
import { executionsApi, resultsApi } from '@/lib/api'
import { Activity, CheckCircle2, XCircle, Clock, Zap } from 'lucide-react'

export function Dashboard() {
  const { data: executions } = useQuery({
    queryKey: ['executions'],
    queryFn: () => executionsApi.list().then((res) => res.data),
    refetchInterval: 5000,
  })

  const { data: activeCount } = useQuery({
    queryKey: ['activeCount'],
    queryFn: () => executionsApi.getActiveCount().then((res) => res.data),
    refetchInterval: 2000,
  })

  const { data: storageStats } = useQuery({
    queryKey: ['storageStats'],
    queryFn: () => resultsApi.getStorageStats().then((res) => res.data),
  })

  const stats = {
    total: executions?.length || 0,
    active: activeCount?.active_executions || 0,
    completed: executions?.filter((e) => e.status === 'completed').length || 0,
    failed: executions?.filter((e) => e.status === 'failed').length || 0,
  }

  const totalTests = executions?.reduce((acc, e) => acc + e.total_tests, 0) || 0
  const passedTests =
    executions?.reduce((acc, e) => acc + e.passed_tests, 0) || 0
  const failedTests =
    executions?.reduce((acc, e) => acc + e.failed_tests, 0) || 0

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Dashboard</h2>
        <p className="mt-2 text-sm text-gray-600">
          Overview of your testing operations
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Executions"
          value={stats.total}
          icon={Activity}
          color="blue"
        />
        <StatCard
          title="Active"
          value={stats.active}
          icon={Zap}
          color="yellow"
        />
        <StatCard
          title="Completed"
          value={stats.completed}
          icon={CheckCircle2}
          color="green"
        />
        <StatCard
          title="Failed"
          value={stats.failed}
          icon={XCircle}
          color="red"
        />
      </div>

      {/* Test Results Summary */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          Test Results Summary
        </h3>
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-gray-900">{totalTests}</div>
            <div className="text-sm text-gray-500">Total Tests</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">
              {passedTests}
            </div>
            <div className="text-sm text-gray-500">Passed</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-red-600">{failedTests}</div>
            <div className="text-sm text-gray-500">Failed</div>
          </div>
        </div>

        {totalTests > 0 && (
          <div className="mt-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-600">Pass Rate</span>
              <span className="text-sm font-medium text-gray-900">
                {((passedTests / totalTests) * 100).toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-green-600 h-2 rounded-full"
                style={{ width: `${(passedTests / totalTests) * 100}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Storage Stats */}
      {storageStats && (
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Storage Statistics
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <div className="text-2xl font-bold text-gray-900">
                {storageStats.total_executions}
              </div>
              <div className="text-sm text-gray-500">Stored Executions</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">
                {storageStats.total_size_mb?.toFixed(2)} MB
              </div>
              <div className="text-sm text-gray-500">Total Storage</div>
            </div>
          </div>
        </div>
      )}

      {/* Recent Executions */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          Recent Executions
        </h3>
        <div className="space-y-3">
          {executions?.slice(0, 5).map((execution) => (
            <div
              key={execution.execution_id}
              className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <div>
                <div className="font-medium text-gray-900">
                  {execution.agent_type}
                </div>
                <div className="text-sm text-gray-500">
                  {new Date(execution.start_time).toLocaleString()}
                </div>
              </div>
              <StatusBadge status={execution.status} />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function StatCard({
  title,
  value,
  icon: Icon,
  color,
}: {
  title: string
  value: number
  icon: any
  color: string
}) {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600',
    yellow: 'bg-yellow-100 text-yellow-600',
    green: 'bg-green-100 text-green-600',
    red: 'bg-red-100 text-red-600',
  }

  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className={`flex-shrink-0 p-3 rounded-md ${colorClasses[color]}`}>
            <Icon className="h-6 w-6" />
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">
                {title}
              </dt>
              <dd className="text-2xl font-bold text-gray-900">{value}</dd>
            </dl>
          </div>
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
      className={`px-2 py-1 text-xs font-medium rounded-full ${
        statusClasses[status] || statusClasses.pending
      }`}
    >
      {status}
    </span>
  )
}
