import React, { useState, useEffect } from 'react'
import { passwordAPI, phishingAPI, vishingAPI } from '../services/api'
import toast from 'react-hot-toast'
import {
  HiOutlineChartBar,
  HiOutlineShieldCheck,
  HiOutlineTrendingUp,
  HiOutlineExclamationCircle,
  HiOutlineSparkles,
  HiOutlineAcademicCap,
  HiOutlineRefresh,
  HiOutlineLockClosed,
  HiOutlineMail,
  HiOutlinePhone
} from 'react-icons/hi'

const Dashboard = () => {
  const [passwordStats, setPasswordStats] = useState(null)
  const [phishingStats, setPhishingStats] = useState(null)
  const [vishingStats, setVishingStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [selectedPeriod, setSelectedPeriod] = useState('week')

  useEffect(() => {
    loadAllStats()
    const interval = setInterval(loadAllStats, 30000)
    return () => clearInterval(interval)
  }, [])

  const loadAllStats = async () => {
    setLoading(true)
    try {
      const [pwdRes, phishRes, vishRes] = await Promise.all([
        passwordAPI.getStats(),
        phishingAPI.getStats(),
        vishingAPI.getStats()
      ])
      
      setPasswordStats(pwdRes.data)
      setPhishingStats(phishRes.data)
      setVishingStats(vishRes.data)
    } catch (error) {
      toast.error('Failed to load dashboard statistics')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <svg className="animate-spin h-12 w-12 text-indigo-600 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  const passwordTotal = passwordStats?.total_attacks ?? passwordStats?.total_analyses ?? 0
  const phishingTotal = phishingStats?.total_emails_analyzed ?? phishingStats?.total_analyses ?? 0
  const vishingTotal = vishingStats?.total_calls_analyzed ?? vishingStats?.total_analyses ?? 0

  const passwordHighRisk = passwordStats?.high_risk_count ?? passwordStats?.successful_cracks ?? 0
  const phishingHighRisk = phishingStats?.high_risk_emails ?? phishingStats?.high_risk_count ?? 0
  const vishingHighRisk = vishingStats?.high_risk_calls ?? vishingStats?.high_risk_count ?? 0

  const passwordStrength = passwordStats?.average_strength ?? Math.max(0, 100 - (passwordStats?.average_risk_score ?? 0))
  const phishingRisk = phishingStats?.average_risk ?? phishingStats?.average_phishing_score ?? 0
  const vishingRisk = vishingStats?.average_risk ?? vishingStats?.average_vishing_score ?? 0

  const totalSimulations = passwordTotal + phishingTotal + vishingTotal
  const totalHighRisk = passwordHighRisk + phishingHighRisk + vishingHighRisk

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <div className="p-2 bg-indigo-100 rounded-lg">
                <HiOutlineChartBar className="text-indigo-600" size={28} />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Security Dashboard</h1>
                <p className="text-gray-600 text-sm mt-1">Cybersecurity Awareness & Risk Analytics</p>
              </div>
            </div>
          </div>
          <button
            onClick={loadAllStats}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200 transition-colors"
            title="Refresh data"
          >
            <HiOutlineRefresh size={18} />
            Refresh
          </button>
        </div>

        {/* Period Selector */}
        <div className="flex gap-2 flex-wrap">
          {['week', 'month', 'year'].map((period) => (
            <button
              key={period}
              onClick={() => setSelectedPeriod(period)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedPeriod === period
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {period === 'week' ? 'This Week' : period === 'month' ? 'This Month' : 'This Year'}
            </button>
          ))}
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Simulations */}
        <div className="card bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-xs font-semibold text-gray-700 mb-1">Total Simulations</p>
              <p className="text-3xl font-bold text-gray-900">{totalSimulations}</p>
              <p className="text-xs text-gray-600 mt-2">Across all modules</p>
            </div>
            <div className="p-3 bg-blue-200 rounded-lg">
              <HiOutlineChartBar size={24} className="text-blue-700" />
            </div>
          </div>
        </div>

        {/* High-Risk Detections */}
        <div className="card bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-xs font-semibold text-gray-700 mb-1">High-Risk Detections</p>
              <p className="text-3xl font-bold text-gray-900">{totalHighRisk}</p>
              <p className="text-xs text-gray-600 mt-2">Vulnerabilities identified</p>
            </div>
            <div className="p-3 bg-orange-200 rounded-lg">
              <HiOutlineExclamationCircle size={24} className="text-orange-700" />
            </div>
          </div>
        </div>

        {/* Average Password Strength */}
        <div className="card bg-gradient-to-br from-cyan-50 to-cyan-100 border-cyan-200">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-xs font-semibold text-gray-700 mb-1">Avg. Password Strength</p>
              <p className="text-3xl font-bold text-gray-900">{Math.round(passwordStrength)}</p>
              <p className="text-xs text-gray-600 mt-2">Out of 100</p>
            </div>
            <div className="p-3 bg-cyan-200 rounded-lg">
              <HiOutlineLockClosed size={24} className="text-cyan-700" />
            </div>
          </div>
        </div>

        {/* Trend */}
        <div className="card bg-gradient-to-br from-emerald-50 to-emerald-100 border-emerald-200">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-xs font-semibold text-gray-700 mb-1">Improvement Trend</p>
              <div className="flex items-baseline gap-1 mt-2">
                <p className="text-3xl font-bold text-emerald-700">↓ 12%</p>
              </div>
              <p className="text-xs text-gray-600 mt-2">Compared to last period</p>
            </div>
            <div className="p-3 bg-emerald-200 rounded-lg">
              <HiOutlineTrendingUp size={24} className="text-emerald-700" />
            </div>
          </div>
        </div>
      </div>

      {/* Analysis Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Password Analysis */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900 flex items-center">
              <HiOutlineLockClosed className="mr-2 text-cyan-600" size={20} />
              Password Analysis
            </h3>
            <span className="badge-info">{passwordTotal}</span>
          </div>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Average Strength</span>
              <span className="text-sm font-bold text-gray-900">{Math.round(passwordStrength)}/100</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-cyan-600 h-2 rounded-full" style={{ width: `${Math.min(passwordStrength, 100)}%` }}></div>
            </div>
            <div className="flex items-center justify-between pt-2">
              <span className="text-sm text-gray-600">High-Risk Passwords</span>
              <span className="text-sm font-bold text-red-600">{passwordHighRisk}</span>
            </div>
          </div>
        </div>

        {/* Phishing Analysis */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900 flex items-center">
              <HiOutlineMail className="mr-2 text-amber-600" size={20} />
              Phishing Analysis
            </h3>
            <span className="badge-warning">{phishingTotal}</span>
          </div>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Average Risk</span>
              <span className="text-sm font-bold text-gray-900">{Math.round(phishingRisk)}/100</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-amber-600 h-2 rounded-full" style={{ width: `${Math.min(phishingRisk, 100)}%` }}></div>
            </div>
            <div className="flex items-center justify-between pt-2">
              <span className="text-sm text-gray-600">High-Risk Emails</span>
              <span className="text-sm font-bold text-red-600">{phishingHighRisk}</span>
            </div>
          </div>
        </div>

        {/* Vishing Analysis */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900 flex items-center">
              <HiOutlinePhone className="mr-2 text-emerald-600" size={20} />
              Vishing Analysis
            </h3>
            <span className="badge-danger">{vishingTotal}</span>
          </div>
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Average Risk</span>
              <span className="text-sm font-bold text-gray-900">{Math.round(vishingRisk)}/100</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-emerald-600 h-2 rounded-full" style={{ width: `${Math.min(vishingRisk, 100)}%` }}></div>
            </div>
            <div className="flex items-center justify-between pt-2">
              <span className="text-sm text-gray-600">High-Risk Calls</span>
              <span className="text-sm font-bold text-red-600">{vishingHighRisk}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="card bg-gradient-to-r from-indigo-50 to-purple-50 border-indigo-200">
        <div className="flex items-start gap-3">
          <HiOutlineSparkles className="text-indigo-600 flex-shrink-0 mt-0.5" size={24} />
          <div className="flex-1">
            <h3 className="text-lg font-bold text-gray-900 mb-3">Personalized Recommendations</h3>
            <ul className="space-y-2">
              {[
                { icon: '🔐', text: 'Strengthen weak passwords - Focus on complexity and uniqueness' },
                { icon: '📧', text: 'Review phishing indicators - Learn to spot urgency tactics' },
                { icon: '☎️', text: 'Study voice phishing patterns - Recognize social engineering in calls' },
                { icon: '✅', text: 'Enable MFA across accounts - Add extra security layer' },
                { icon: '📚', text: 'Complete security awareness training - Improve overall literacy score' }
              ].map((rec, idx) => (
                <li key={idx} className="flex items-center text-sm text-gray-700">
                  <span className="mr-3 text-lg">{rec.icon}</span>
                  <span>{rec.text}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Statistics Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Pattern Frequencies */}
        <div className="card">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Most Common Patterns</h3>
          <div className="space-y-2">
            {[
              { pattern: 'Sequential Characters (123, abc)', count: 15 },
              { pattern: 'Dictionary Words', count: 12 },
              { pattern: 'Urgency Tactics', count: 10 },
              { pattern: 'Authority Impersonation', count: 8 }
            ].map((item, idx) => (
              <div key={idx} className="flex items-center justify-between">
                <span className="text-sm text-gray-700">{item.pattern}</span>
                <span className="text-sm font-bold text-indigo-600">{item.count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Risk Status */}
        <div className="card">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Overall Risk Status</h3>
          <div className="space-y-3">
            <div className="p-3 bg-green-50 rounded-lg border border-green-200">
              <p className="text-sm font-semibold text-green-700">✓ Strengths</p>
              <p className="text-xs text-gray-600 mt-1">Good awareness of phishing tactics, consistent training engagement</p>
            </div>
            <div className="p-3 bg-orange-50 rounded-lg border border-orange-200">
              <p className="text-sm font-semibold text-orange-700">⚠ Areas for Improvement</p>
              <p className="text-xs text-gray-600 mt-1">Password complexity needs work, vishing detection rate below target</p>
            </div>
          </div>
        </div>
      </div>

      {/* Last Updated */}
      <div className="text-center text-xs text-gray-500 mb-4">
        Dashboard data last refreshed • Real-time updates every 30 seconds
      </div>
    </div>
  )
}

export default Dashboard
