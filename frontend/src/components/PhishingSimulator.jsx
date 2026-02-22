import React, { useState, useEffect } from 'react'
import { phishingAPI } from '../services/api'
import toast from 'react-hot-toast'
import { HiOutlineMail, HiOutlineExclamationCircle, HiOutlineInformationCircle, HiOutlineShieldCheck, HiOutlineRefresh } from 'react-icons/hi'

const PhishingSimulator = () => {
  const [formData, setFormData] = useState({
    emailSubject: '',
    emailBody: '',
    senderEmail: '',
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState([])

  useEffect(() => {
    loadHistory()
    
    // Real-time history updates every 10 seconds
    const interval = setInterval(() => {
      loadHistory()
    }, 10000)

    return () => clearInterval(interval)
  }, [])

  const loadHistory = async () => {
    try {
      const response = await phishingAPI.getHistory(10)
      setHistory(response.data)
    } catch (error) {
      console.error('Failed to load history:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.emailSubject.trim() || !formData.emailBody.trim()) {
      toast.error('Please fill in all required fields')
      return
    }
    
    setLoading(true)
    setResult(null)

    try {
      const response = await phishingAPI.analyze({
        email_subject: formData.emailSubject,
        email_body: formData.emailBody,
        sender_email: formData.senderEmail,
      })

      setResult(response.data)
      toast.success('Phishing analysis complete!')
      loadHistory()
      setTimeout(() => {
        document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 100)
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Analysis failed')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const loadSampleEmail = (type) => {
    const samples = {
      phishing: {
        subject: 'URGENT: Your Account Will Be Suspended',
        body: 'Dear Customer, We have detected suspicious activity on your account. Please verify your identity immediately by clicking the link below. Failure to do so within 24 hours will result in account suspension. Click here to verify: https://fake-bank-verify.com',
        sender: 'security@bank-verify.com',
      },
      legitimate: {
        subject: 'Monthly Statement Available',
        body: 'Your monthly account statement is now available for download. You can access it through your online banking portal. If you have any questions, please contact our customer service team.',
        sender: 'noreply@yourbank.com',
      },
    }

    setFormData({
      emailSubject: samples[type].subject,
      emailBody: samples[type].body,
      senderEmail: samples[type].sender,
    })
  }

  const getRiskColor = (score) => {
    if (score >= 80) return 'text-red-700 bg-red-50 border-red-200'
    if (score >= 60) return 'text-orange-700 bg-orange-50 border-orange-200'
    if (score >= 40) return 'text-yellow-700 bg-yellow-50 border-yellow-200'
    return 'text-green-700 bg-green-50 border-green-200'
  }

  const getRiskLabel = (score) => {
    if (score >= 80) return 'Critical Risk'
    if (score >= 60) return 'High Risk'
    if (score >= 40) return 'Medium Risk'
    return 'Low Risk'
  }

  const getRiskBadge = (score) => {
    if (score >= 80) return 'badge-danger'
    if (score >= 60) return 'badge-warning'
    return 'badge-success'
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header Section */}
      <div className="card">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
          <div className="mb-4 sm:mb-0">
            <div className="flex items-center space-x-3 mb-2">
              <div className="p-2 bg-purple-100 rounded-lg">
                <HiOutlineMail className="text-purple-600" size={24} />
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">Phishing & Social Engineering Simulator</h2>
            </div>
            <p className="text-gray-600 mt-2 text-sm sm:text-base">
              Analyze emails for phishing indicators, urgency manipulation, and social engineering tactics using AI-powered detection.
            </p>
          </div>
        </div>

        {/* Sample Email Buttons */}
        <div className="mb-6 flex flex-wrap gap-3">
          <button
            onClick={() => loadSampleEmail('phishing')}
            className="btn-secondary bg-red-50 text-red-700 hover:bg-red-100 border-red-200"
          >
            Load Sample Phishing Email
          </button>
          <button
            onClick={() => loadSampleEmail('legitimate')}
            className="btn-secondary bg-green-50 text-green-700 hover:bg-green-100 border-green-200"
          >
            Load Sample Legitimate Email
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid grid-cols-1 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Sender Email Address
              </label>
              <input
                type="email"
                value={formData.senderEmail}
                onChange={(e) => setFormData({ ...formData, senderEmail: e.target.value })}
                className="input-field"
                placeholder="sender@example.com"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Email Subject <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={formData.emailSubject}
                onChange={(e) => setFormData({ ...formData, emailSubject: e.target.value })}
                className="input-field"
                placeholder="Enter email subject"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Email Body Content <span className="text-red-500">*</span>
              </label>
              <textarea
                value={formData.emailBody}
                onChange={(e) => setFormData({ ...formData, emailBody: e.target.value })}
                className="textarea-field"
                rows="8"
                placeholder="Enter email body content..."
                required
              />
            </div>
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
              'Analyze Email'
            )}
          </button>
        </form>
      </div>

      {/* Results Section */}
      {result && (
        <div id="results-section" className="card animate-slide-up">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
            <h3 className="text-xl sm:text-2xl font-bold text-gray-900 flex items-center mb-2 sm:mb-0">
              <HiOutlineShieldCheck className="mr-2 text-purple-600" size={24} />
              Analysis Results
            </h3>
            <span className={`badge ${getRiskBadge(result.overall_risk.overall_risk)}`}>
              {getRiskLabel(result.overall_risk.overall_risk)}
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div className={`card border-2 ${getRiskColor(result.overall_risk.overall_risk)}`}>
              <p className="text-xs font-medium text-gray-600 mb-1">Phishing Risk</p>
              <p className="text-2xl sm:text-3xl font-bold">{getRiskLabel(result.overall_risk.overall_risk)}</p>
              <p className="text-xs text-gray-500 mt-1">Score: {result.overall_risk.overall_risk.toFixed(1)}/100</p>
            </div>

            <div className="card bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
              <p className="text-xs font-medium text-gray-600 mb-1">Click Rate</p>
              <p className="text-2xl sm:text-3xl font-bold text-gray-900">{result.click_rate_simulation.toFixed(1)}%</p>
              <p className="text-xs text-gray-500 mt-1">Estimated likelihood</p>
            </div>

            <div className="card bg-orange-50 border-orange-200">
              <p className="text-xs font-medium text-gray-600 mb-1">Urgency Score</p>
              <p className="text-2xl sm:text-3xl font-bold text-gray-900">{result.urgency_score.toFixed(1)}</p>
              <p className="text-xs text-gray-500 mt-1">/100</p>
            </div>

            <div className="card bg-purple-50 border-purple-200">
              <p className="text-xs font-medium text-gray-600 mb-1">Emotional Manipulation</p>
              <p className="text-2xl sm:text-3xl font-bold text-gray-900">{result.emotional_manipulation_score.toFixed(1)}</p>
              <p className="text-xs text-gray-500 mt-1">/100</p>
            </div>
          </div>

          {/* Progress Bars */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
            <div className="card">
              <div className="flex items-center justify-between mb-2">
                <p className="text-sm font-semibold text-gray-700">Urgency Indicators</p>
                <span className="text-sm font-bold text-orange-600">{result.urgency_score.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-orange-600 h-3 rounded-full transition-all duration-500"
                  style={{ width: `${result.urgency_score}%` }}
                ></div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center justify-between mb-2">
                <p className="text-sm font-semibold text-gray-700">Emotional Manipulation</p>
                <span className="text-sm font-bold text-purple-600">{result.emotional_manipulation_score.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-purple-600 h-3 rounded-full transition-all duration-500"
                  style={{ width: `${result.emotional_manipulation_score}%` }}
                ></div>
              </div>
            </div>
          </div>

          {result.suspicious_keywords && result.suspicious_keywords.length > 0 && (
            <div className="mb-6 card bg-red-50 border-red-200">
              <h4 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                <HiOutlineExclamationCircle className="mr-2 text-red-600" size={20} />
                Suspicious Keywords Detected
              </h4>
              <div className="flex flex-wrap gap-2">
                {result.suspicious_keywords.map((keyword, idx) => (
                  <span key={idx} className="badge-danger capitalize">
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}

          {result.sender_analysis && (
            <div className="mb-6 card bg-gray-50">
              <h4 className="text-lg font-bold text-gray-900 mb-3">Sender Analysis</h4>
              <div className="space-y-2">
                <p className="text-sm text-gray-700">
                  <strong className="text-gray-900">Sender:</strong> {result.sender_analysis.sender || 'Not provided'}
                </p>
                {result.sender_analysis.suspicious_domain && (
                  <div className="flex items-center text-sm text-red-600 bg-red-50 p-2 rounded-lg">
                    <HiOutlineExclamationCircle className="mr-2" size={16} />
                    ⚠️ Suspicious domain pattern detected
                  </div>
                )}
              </div>
            </div>
          )}

          {result.recommendations && result.recommendations.length > 0 && (
            <div className="mb-6 card bg-blue-50 border-blue-200">
              <h4 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                <HiOutlineInformationCircle className="mr-2 text-blue-600" size={20} />
                Security Recommendations
              </h4>
              <ul className="space-y-2">
                {result.recommendations.map((rec, idx) => (
                  <li key={idx} className="flex items-start text-sm text-gray-700">
                    <span className="text-blue-600 mr-2">•</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {result.overall_risk.factors && result.overall_risk.factors.length > 0 && (
            <div className="card bg-yellow-50 border-yellow-200">
              <h4 className="text-lg font-bold text-gray-900 mb-3">Risk Factors</h4>
              <ul className="space-y-2">
                {result.overall_risk.factors.map((factor, idx) => (
                  <li key={idx} className="flex items-start text-sm text-gray-700">
                    <span className="text-yellow-600 mr-2">•</span>
                    <span>{factor}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* History Section */}
      {history.length > 0 && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl sm:text-2xl font-bold text-gray-900">Recent Analysis History</h3>
            <button
              onClick={loadHistory}
              className="flex items-center gap-2 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium"
              title="Refresh history"
            >
              <HiOutlineRefresh size={16} />
              Refresh
            </button>
          </div>
          <div className="overflow-x-auto scrollbar-hide">
            <div className="inline-block min-w-full align-middle">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Subject</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider hidden sm:table-cell">Sender</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Risk</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider hidden md:table-cell">Click Rate</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {history.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 text-sm font-medium text-gray-900 max-w-xs truncate">
                        {item.email_subject}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600 hidden sm:table-cell">
                        {item.sender_email}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span className={`badge ${getRiskBadge(item.phishing_score)}`}>
                          {item.phishing_score.toFixed(1)}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600 hidden md:table-cell">
                        {item.click_rate_simulation.toFixed(1)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default PhishingSimulator
