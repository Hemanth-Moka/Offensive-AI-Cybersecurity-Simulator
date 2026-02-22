import React, { useState } from 'react'
import { userBehaviorAPI } from '../services/api'
import toast from 'react-hot-toast'
import { HiOutlineUser, HiOutlineShieldCheck, HiOutlineChartBar, HiOutlineExclamationCircle } from 'react-icons/hi'

const UserBehaviorAnalysis = () => {
  const [userId, setUserId] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async (e) => {
    e.preventDefault()
    if (!userId.trim()) {
      toast.error('Please enter a user ID')
      return
    }

    setLoading(true)
    setResult(null)

    try {
      const response = await userBehaviorAPI.analyze({
        user_id: userId,
      })

      setResult(response.data)
      toast.success('User behavior analysis complete!')
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Analysis failed')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const getAwarenessColor = (score) => {
    if (score >= 70) return 'text-green-700 bg-green-50 border-green-200'
    if (score >= 50) return 'text-yellow-700 bg-yellow-50 border-yellow-200'
    return 'text-red-700 bg-red-50 border-red-200'
  }

  const getAwarenessLabel = (score) => {
    if (score >= 70) return 'High Awareness'
    if (score >= 50) return 'Moderate Awareness'
    return 'Low Awareness'
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header Section */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-6">
          <div className="p-2 bg-indigo-100 rounded-lg">
            <HiOutlineUser className="text-indigo-600" size={50} />
          </div>
          <div>
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mt-2">User Behavior Analysis</h2>
            <p className="text-gray-600 mt-1 text-sm sm:text ">
              AI-powered analysis of user behavior patterns, security awareness, and personalized training recommendations.
            </p>
          </div>
        </div>

        <form onSubmit={handleAnalyze} className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              User ID <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              className="input-field"
              placeholder="Enter user ID to analyze"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              The system will analyze historical password attacks, phishing, and vishing data for this user.
            </p>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full sm:w-auto"
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </span>
            ) : (
              'Analyze User Behavior'
            )}
          </button>
        </form>
      </div>

      {/* Results Section */}
      {result && (
        <div className="card animate-slide-up">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl sm:text-2xl font-bold text-gray-900 flex items-center">
              <HiOutlineShieldCheck className="mr-2 text-indigo-600" size={24} />
              Analysis Results
            </h3>
            <span className={`badge ${result.risk_profile.risk_level === 'Low' ? 'badge-success' : result.risk_profile.risk_level === 'Medium' ? 'badge-warning' : 'badge-danger'}`}>
              {result.risk_profile.risk_level} Risk
            </span>
          </div>

          {/* Key Metrics */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div className={`card border-2 ${getAwarenessColor(result.awareness_level)}`}>
              <p className="text-xs font-medium text-gray-600 mb-1">Awareness Level</p>
              <p className="text-2xl sm:text-3xl font-bold">{getAwarenessLabel(result.awareness_level)}</p>
              <p className="text-xs text-gray-500 mt-1">Score: {result.awareness_level.toFixed(1)}/100</p>
            </div>

            <div className="card bg-orange-50 border-orange-200">
              <p className="text-xs font-medium text-gray-600 mb-1">Phishing Susceptibility</p>
              <p className="text-2xl sm:text-3xl font-bold text-gray-900">{result.phishing_susceptibility.toFixed(1)}</p>
              <p className="text-xs text-gray-500 mt-1">/100</p>
            </div>

            <div className="card bg-red-50 border-red-200">
              <p className="text-xs font-medium text-gray-600 mb-1">Password Risk</p>
              <p className="text-2xl sm:text-3xl font-bold text-gray-900">{result.risk_profile.password_risk.toFixed(1)}</p>
              <p className="text-xs text-gray-500 mt-1">/100</p>
            </div>

            <div className="card bg-purple-50 border-purple-200">
              <p className="text-xs font-medium text-gray-600 mb-1">Overall Risk</p>
              <p className="text-2xl sm:text-3xl font-bold text-gray-900">{result.risk_profile.overall_risk.toFixed(1)}</p>
              <p className="text-xs text-gray-500 mt-1">/100</p>
            </div>
          </div>

          {/* Behavior Insights */}
          {result.behavior_insights && (
            <div className="mb-6 card bg-blue-50 border-blue-200">
              <h4 className="text-lg font-bold text-gray-900 mb-3">Behavior Insights</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm font-semibold text-gray-700 mb-2">Common Password Patterns</p>
                  <div className="flex flex-wrap gap-2">
                    {result.behavior_insights.common_password_patterns?.length > 0 ? (
                      result.behavior_insights.common_password_patterns.map((pattern, idx) => (
                        <span key={idx} className="badge-warning capitalize">
                          {pattern}
                        </span>
                      ))
                    ) : (
                      <span className="text-sm text-gray-500">No patterns detected</span>
                    )}
                  </div>
                </div>
                <div>
                  <p className="text-sm font-semibold text-gray-700 mb-2">Statistics</p>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>Weak Password Ratio: {result.behavior_insights.weak_password_ratio}%</li>
                    <li>Average Password Strength: {result.behavior_insights.average_password_strength}/100</li>
                    <li>Total Analyses: {result.behavior_insights.total_analyses}</li>
                    <li>High Risk Incidents: {result.behavior_insights.high_risk_incidents}</li>
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* Training Recommendations */}
          {result.training_recommendations && result.training_recommendations.length > 0 && (
            <div className="card bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
              <h4 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                <HiOutlineExclamationCircle className="mr-2 text-blue-600" size={20} />
                Awareness Training Recommendations
              </h4>
              <ul className="space-y-2">
                {result.training_recommendations.map((rec, idx) => (
                  <li key={idx} className="flex items-start text-sm text-gray-700 bg-white p-3 rounded-lg">
                    <span className="text-blue-600 mr-2 font-bold">•</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Risk Profile */}
          <div className="mt-6 card bg-gray-50">
            <h4 className="text-lg font-bold text-gray-900 mb-3">Risk Profile</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-2">Risk Breakdown</p>
                <div className="space-y-2">
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className="text-xs text-gray-600">Password Risk</span>
                      <span className="text-xs font-bold">{result.risk_profile.password_risk.toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-red-500 h-2 rounded-full"
                        style={{ width: `${result.risk_profile.password_risk}%` }}
                      ></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className="text-xs text-gray-600">Phishing Risk</span>
                      <span className="text-xs font-bold">{result.risk_profile.phishing_risk.toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-orange-500 h-2 rounded-full"
                        style={{ width: `${result.risk_profile.phishing_risk}%` }}
                      ></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className="text-xs text-gray-600">Vishing Risk</span>
                      <span className="text-xs font-bold">{result.risk_profile.vishing_risk.toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-purple-500 h-2 rounded-full"
                        style={{ width: `${result.risk_profile.vishing_risk}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-2">Risk Level</p>
                <div className={`p-4 rounded-lg border-2 ${
                  result.risk_profile.risk_level === 'Low' ? 'bg-green-50 border-green-200' :
                  result.risk_profile.risk_level === 'Medium' ? 'bg-yellow-50 border-yellow-200' :
                  result.risk_profile.risk_level === 'High' ? 'bg-orange-50 border-orange-200' :
                  'bg-red-50 border-red-200'
                }`}>
                  <p className="text-2xl font-bold">{result.risk_profile.risk_level}</p>
                  <p className="text-sm text-gray-600 mt-1">Overall Risk Score: {result.risk_profile.overall_risk.toFixed(1)}/100</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default UserBehaviorAnalysis
