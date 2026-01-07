import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { resultsApi } from '@/lib/api'
import {
  CheckCircle2,
  XCircle,
  AlertCircle,
  FileText,
  Lightbulb,
  Code,
} from 'lucide-react'

export function ResultsViewer() {
  const { executionId } = useParams()

  const { data: summary } = useQuery({
    queryKey: ['summary', executionId],
    queryFn: () =>
      executionId ? resultsApi.getSummary(executionId).then((r) => r.data) : null,
    enabled: !!executionId,
  })

  const { data: testCases } = useQuery({
    queryKey: ['testCases', executionId],
    queryFn: () =>
      executionId
        ? resultsApi.getTestCases(executionId).then((r) => r.data)
        : null,
    enabled: !!executionId,
  })

  const { data: rca } = useQuery({
    queryKey: ['rca', executionId],
    queryFn: () =>
      executionId ? resultsApi.getRCA(executionId).then((r) => r.data) : null,
    enabled: !!executionId,
  })

  const { data: recommendations } = useQuery({
    queryKey: ['recommendations', executionId],
    queryFn: () =>
      executionId
        ? resultsApi.getRecommendations(executionId).then((r) => r.data)
        : null,
    enabled: !!executionId,
  })

  if (!executionId) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Select an execution to view results</p>
      </div>
    )
  }

  if (!summary) {
    return <div className="text-center py-12">Loading...</div>
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Test Results</h2>
        <p className="mt-2 text-sm text-gray-600">{summary.agent_type}</p>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          title="Total Tests"
          value={summary.summary.total_tests}
          icon={FileText}
        />
        <StatCard
          title="Passed"
          value={summary.summary.passed_tests}
          icon={CheckCircle2}
          color="green"
        />
        <StatCard
          title="Failed"
          value={summary.summary.failed_tests}
          icon={XCircle}
          color="red"
        />
        <StatCard
          title="Pass Rate"
          value={`${summary.summary.pass_rate.toFixed(1)}%`}
          icon={CheckCircle2}
          color="blue"
        />
      </div>

      {/* Test Cases */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Test Cases</h3>
        </div>
        <div className="divide-y divide-gray-200">
          {testCases?.test_cases.map((tc: any) => (
            <div key={tc.id} className="px-6 py-4">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    {tc.status === 'passed' ? (
                      <CheckCircle2 className="h-5 w-5 text-green-500" />
                    ) : tc.status === 'failed' ? (
                      <XCircle className="h-5 w-5 text-red-500" />
                    ) : (
                      <AlertCircle className="h-5 w-5 text-gray-500" />
                    )}
                    <span className="font-medium text-gray-900">{tc.name}</span>
                  </div>
                  <p className="mt-1 text-sm text-gray-500">{tc.description}</p>
                  {tc.error_message && (
                    <div className="mt-2 p-2 bg-red-50 rounded text-sm text-red-700">
                      {tc.error_message}
                    </div>
                  )}
                </div>
                {tc.execution_time && (
                  <span className="text-sm text-gray-500">
                    {tc.execution_time.toFixed(3)}s
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Root Cause Analysis */}
      {rca && rca.total_issues > 0 && (
        <div className="bg-white shadow rounded-lg overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">
              Root Cause Analysis
            </h3>
          </div>
          <div className="divide-y divide-gray-200">
            {rca.rca_results.map((item: any) => (
              <div key={item.issue_id} className="px-6 py-4">
                <div className="flex items-start space-x-3">
                  <AlertCircle className="h-5 w-5 text-red-500 mt-0.5" />
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <span className="font-medium text-gray-900">
                        {item.category}
                      </span>
                      <SeverityBadge severity={item.severity} />
                    </div>
                    <p className="mt-1 text-sm text-gray-600">
                      {item.root_cause}
                    </p>
                    <div className="mt-2 text-sm text-gray-500">
                      Affected: {item.affected_components.join(', ')}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {recommendations && recommendations.total_recommendations > 0 && (
        <div className="bg-white shadow rounded-lg overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">
              Recommendations
            </h3>
          </div>
          <div className="divide-y divide-gray-200">
            {recommendations.recommendations.map((rec: any) => (
              <div key={rec.recommendation_id} className="px-6 py-4">
                <div className="flex items-start space-x-3">
                  <Lightbulb className="h-5 w-5 text-yellow-500 mt-0.5" />
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <span className="font-medium text-gray-900">
                        {rec.title}
                      </span>
                      <SeverityBadge severity={rec.priority} />
                    </div>
                    <p className="mt-1 text-sm text-gray-600">
                      {rec.description}
                    </p>
                    <div className="mt-2 p-3 bg-blue-50 rounded">
                      <div className="flex items-start space-x-2">
                        <Code className="h-4 w-4 text-blue-600 mt-0.5" />
                        <div className="text-sm text-blue-900">
                          <div className="font-medium">Suggested Fix:</div>
                          <div className="mt-1">{rec.suggested_fix}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function StatCard({
  title,
  value,
  icon: Icon,
  color = 'gray',
}: {
  title: string
  value: number | string
  icon: any
  color?: string
}) {
  const colorClasses = {
    gray: 'bg-gray-100 text-gray-600',
    green: 'bg-green-100 text-green-600',
    red: 'bg-red-100 text-red-600',
    blue: 'bg-blue-100 text-blue-600',
  }

  return (
    <div className="bg-white overflow-hidden shadow rounded-lg p-5">
      <div className="flex items-center">
        <div className={`p-3 rounded-md ${colorClasses[color]}`}>
          <Icon className="h-6 w-6" />
        </div>
        <div className="ml-5">
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
      </div>
    </div>
  )
}

function SeverityBadge({ severity }: { severity: string }) {
  const severityClasses = {
    low: 'bg-blue-100 text-blue-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-orange-100 text-orange-800',
    critical: 'bg-red-100 text-red-800',
  }

  return (
    <span
      className={`px-2 py-0.5 text-xs font-medium rounded-full ${
        severityClasses[severity] || severityClasses.medium
      }`}
    >
      {severity}
    </span>
  )
}
