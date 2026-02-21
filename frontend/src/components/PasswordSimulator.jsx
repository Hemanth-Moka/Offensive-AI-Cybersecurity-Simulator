import React, { useState, useEffect } from 'react'
import { passwordAPI } from '../services/api'
import toast from 'react-hot-toast'
import { HiOutlineLockClosed, HiOutlineKey, HiOutlineShieldCheck, HiOutlineExclamationCircle, HiOutlineInformationCircle } from 'react-icons/hi'

const PasswordSimulator = () => {
  const [formData, setFormData] = useState({
    password: '',
    hashType: 'MD5',
    attackType: 'dictionary',
    userMetadata: { name: '', dob: '' },
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState([])
  const [showMetadata, setShowMetadata] = useState(false)
  const [activeTab, setActiveTab] = useState('analyze')

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    try {
      const response = await passwordAPI.getHistory(10)
      setHistory(response.data)
    } catch (error) {
      console.error('Failed to load history:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.password.trim()) {
      toast.error('Please enter a password')
      return
    }
    
    setLoading(true)
    setResult(null)

    try {
      const response = await passwordAPI.analyze({
        password: formData.password,
        hash_type: formData.hashType,
        attack_type: formData.attackType,
        user_metadata: showMetadata && (formData.userMetadata.name || formData.userMetadata.dob)
          ? formData.userMetadata
          : null,
      })

      setResult(response.data)
      toast.success('Password analysis complete!')
      loadHistory()
      // Scroll to results
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

  const handleHashCrack = async (e) => {
    e.preventDefault()
    const hashValue = e.target.hash.value.trim()
    if (!hashValue) {
      toast.error('Please enter a hash value')
      return
    }
    
    setLoading(true)
    setResult(null)

    const hashType = e.target.hashType.value
    const attackType = e.target.attackType.value

    try {
      const response = await passwordAPI.crackHash({
        hash_value: hashValue,
        hash_type: hashType,
        attack_type: attackType,
        user_metadata: null,
      })

      setResult(response.data)
      toast.success('Hash analysis complete!')
      loadHistory()
      setTimeout(() => {
        document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 100)
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Hash cracking failed')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = (score) => {
    if (score >= 80) return 'text-red-700 bg-red-50 border-red-200'
    if (score >= 60) return 'text-orange-700 bg-orange-50 border-orange-200'
    if (score >= 40) return 'text-yellow-700 bg-yellow-50 border-yellow-200'
    return 'text-green-700 bg-green-50 border-green-200'
  }

  const getRiskLabel = (score) => {
    if (score >= 80) return 'Critical'
    if (score >= 60) return 'High'
    if (score >= 40) return 'Medium'
    if (score >= 20) return 'Low'
    return 'Very Low'
  }

  const getRiskBadge = (score) => {
    if (score >= 80) return 'badge-danger'
    if (score >= 60) return 'badge-warning'
    if (score >= 40) return 'badge-warning'
    return 'badge-success'
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header Section */}
      <div className="card">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
          <div className="mb-4 sm:mb-0">
            <div className="flex items-center space-x-3 mb-2">
              <div className="p-2 bg-blue-100 rounded-lg">
                <HiOutlineLockClosed className="text-blue-600" size={24} />
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">Password Attack Simulator</h2>
            </div>
            <p className="text-gray-600 mt-2 text-sm sm:text-base">
              Simulate password attacks to analyze password strength and vulnerability patterns using advanced AI algorithms.
            </p>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-2 border-b border-gray-200 mb-6">
          <button
            onClick={() => setActiveTab('analyze')}
            className={`px-4 py-2 font-medium text-sm transition-colors border-b-2 ${
              activeTab === 'analyze'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            Analyze Password
          </button>
          <button
            onClick={() => setActiveTab('crack')}
            className={`px-4 py-2 font-medium text-sm transition-colors border-b-2 ${
              activeTab === 'crack'
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            Crack Hash
          </button>
        </div>

        {/* Forms */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Password Analysis Form */}
          {activeTab === 'analyze' && (
            <div className="lg:col-span-2">
              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="sm:col-span-2">
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Password to Analyze
                    </label>
                    <div className="relative">
                      <input
                        type="text"
                        value={formData.password}
                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                        className="input-field pr-10"
                        placeholder="Enter password to analyze"
                        required
                      />
                      <HiOutlineKey className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Hash Algorithm
                    </label>
                    <select
                      value={formData.hashType}
                      onChange={(e) => setFormData({ ...formData, hashType: e.target.value })}
                      className="input-field"
                    >
                      <option value="MD5">MD5</option>
                      <option value="SHA256">SHA256</option>
                      <option value="bcrypt">bcrypt</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Attack Type
                    </label>
                    <select
                      value={formData.attackType}
                      onChange={(e) => setFormData({ ...formData, attackType: e.target.value })}
                      className="input-field"
                    >
                      <option value="dictionary">Dictionary Attack</option>
                      <option value="brute_force">Brute Force (Limited)</option>
                      <option value="hybrid">Hybrid Attack</option>
                      <option value="ai_guided">AI-Guided Attack</option>
                    </select>
                  </div>
                </div>

                <div className="border-t border-gray-200 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowMetadata(!showMetadata)}
                    className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center"
                  >
                    <HiOutlineInformationCircle className="mr-1" size={16} />
                    {showMetadata ? 'Hide' : 'Show'} User Metadata (for AI-guided attacks)
                  </button>
                  {showMetadata && (
                    <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
                      <input
                        type="text"
                        placeholder="Name"
                        value={formData.userMetadata.name}
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            userMetadata: { ...formData.userMetadata, name: e.target.value },
                          })
                        }
                        className="input-field"
                      />
                      <input
                        type="text"
                        placeholder="Date of Birth (YYYY-MM-DD)"
                        value={formData.userMetadata.dob}
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            userMetadata: { ...formData.userMetadata, dob: e.target.value },
                          })
                        }
                        className="input-field"
                      />
                    </div>
                  )}
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
                    'Analyze Password'
                  )}
                </button>
              </form>
            </div>
          )}

          {/* Hash Cracking Form */}
          {activeTab === 'crack' && (
            <div className="lg:col-span-2">
              <form onSubmit={handleHashCrack} className="space-y-5">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="sm:col-span-2">
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Hash Value
                    </label>
                    <input
                      type="text"
                      name="hash"
                      className="input-field font-mono text-sm"
                      placeholder="Enter hash value to crack"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Hash Algorithm
                    </label>
                    <select
                      name="hashType"
                      className="input-field"
                    >
                      <option value="MD5">MD5</option>
                      <option value="SHA256">SHA256</option>
                      <option value="bcrypt">bcrypt</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Attack Type
                    </label>
                    <select
                      name="attackType"
                      className="input-field"
                    >
                      <option value="dictionary">Dictionary Attack</option>
                      <option value="brute_force">Brute Force (Limited)</option>
                      <option value="hybrid">Hybrid Attack</option>
                      <option value="ai_guided">AI-Guided Attack</option>
                    </select>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary w-full sm:w-auto bg-purple-600 hover:bg-purple-700 focus:ring-purple-500"
                >
                  {loading ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Cracking...
                    </span>
                  ) : (
                    'Crack Hash'
                  )}
                </button>
              </form>
            </div>
          )}
        </div>
      </div>

      {/* Results Section */}
      {result && (
        <div id="results-section" className="card animate-slide-up">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl sm:text-2xl font-bold text-gray-900 flex items-center">
              <HiOutlineShieldCheck className="mr-2 text-blue-600" size={24} />
              Analysis Results
            </h3>
            <span className={`badge ${getRiskBadge(result.overall_risk.overall_risk)}`}>
              {getRiskLabel(result.overall_risk.overall_risk)} Risk
            </span>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div className={`card border-2 ${getRiskColor(result.overall_risk.overall_risk)}`}>
              <p className="text-xs font-medium text-gray-600 mb-1">Risk Level</p>
              <p className="text-2xl sm:text-3xl font-bold">{getRiskLabel(result.overall_risk.overall_risk)}</p>
              <p className="text-xs text-gray-500 mt-1">Score: {result.overall_risk.overall_risk.toFixed(1)}/100</p>
            </div>

            <div className="card bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
              <p className="text-xs font-medium text-gray-600 mb-1">Attack Type</p>
              <p className="text-lg sm:text-xl font-bold text-gray-900 capitalize">
                {result.attack_type.replace('_', ' ')}
              </p>
              <p className="text-xs text-gray-500 mt-1">Simulation Mode</p>
            </div>

            <div className="card bg-gray-50">
              <p className="text-xs font-medium text-gray-600 mb-1">Attempts</p>
              <p className="text-2xl sm:text-3xl font-bold text-gray-900">{result.attempts}</p>
              <p className="text-xs text-gray-500 mt-1">Total guesses</p>
            </div>

            <div className="card bg-gray-50">
              <p className="text-xs font-medium text-gray-600 mb-1">Time Taken</p>
              <p className="text-2xl sm:text-3xl font-bold text-gray-900">{result.time_taken.toFixed(3)}s</p>
              <p className="text-xs text-gray-500 mt-1">Processing time</p>
            </div>
          </div>

          {result.cracked && (
            <div className="mb-6 p-4 bg-gradient-to-r from-red-50 to-red-100 border-2 border-red-300 rounded-xl">
              <div className="flex items-start">
                <HiOutlineExclamationCircle className="text-red-600 flex-shrink-0 mt-0.5 mr-3" size={24} />
                <div className="flex-1">
                  <p className="text-red-900 font-bold text-lg mb-1">⚠️ Password Successfully Cracked!</p>
                  <p className="text-red-800 text-sm mb-2">The password was vulnerable to the selected attack method.</p>
                  <div className="bg-white rounded-lg p-3 mt-2">
                    <p className="text-xs text-gray-600 mb-1">Cracked Password:</p>
                    <code className="text-red-700 font-mono font-bold text-lg">{result.cracked}</code>
                  </div>
                </div>
              </div>
            </div>
          )}

          {result.pattern_analysis && Object.keys(result.pattern_analysis).length > 0 && (
            <div className="mb-6">
              <h4 className="text-lg font-bold text-gray-900 mb-4">Pattern Analysis</h4>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
                <div className="card text-center">
                  <p className="text-xs text-gray-600 mb-1">Strength</p>
                  <p className="text-2xl font-bold text-gray-900">{result.pattern_analysis.strength_score || 'N/A'}</p>
                  <p className="text-xs text-gray-500 mt-1">/100</p>
                </div>
                <div className="card text-center">
                  <p className="text-xs text-gray-600 mb-1">Length</p>
                  <p className="text-2xl font-bold text-gray-900">{result.pattern_analysis.length || 'N/A'}</p>
                  <p className="text-xs text-gray-500 mt-1">characters</p>
                </div>
                <div className="card text-center">
                  <p className="text-xs text-gray-600 mb-1">Complexity</p>
                  <p className="text-2xl font-bold text-gray-900">{result.pattern_analysis.complexity || 'N/A'}</p>
                  <p className="text-xs text-gray-500 mt-1">/4 types</p>
                </div>
                <div className="card text-center">
                  <p className="text-xs text-gray-600 mb-1">Patterns</p>
                  <p className="text-2xl font-bold text-gray-900">{result.pattern_analysis.patterns_found?.length || 0}</p>
                  <p className="text-xs text-gray-500 mt-1">detected</p>
                </div>
              </div>
              
              {result.pattern_analysis.patterns_found?.length > 0 && (
                <div className="card bg-yellow-50 border-yellow-200">
                  <p className="text-sm font-semibold text-gray-900 mb-2">Detected Weak Patterns:</p>
                  <div className="flex flex-wrap gap-2">
                    {result.pattern_analysis.patterns_found.map((pattern, idx) => (
                      <span key={idx} className="badge-warning capitalize">
                        {pattern.replace('_', ' ')}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {result.overall_risk.recommendations && result.overall_risk.recommendations.length > 0 && (
            <div className="card bg-blue-50 border-blue-200">
              <h4 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                <HiOutlineInformationCircle className="mr-2 text-blue-600" size={20} />
                Security Recommendations
              </h4>
              <ul className="space-y-2">
                {result.overall_risk.recommendations.map((rec, idx) => (
                  <li key={idx} className="flex items-start text-sm text-gray-700">
                    <span className="text-blue-600 mr-2">•</span>
                    <span>{rec}</span>
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
          <h3 className="text-xl sm:text-2xl font-bold text-gray-900 mb-4">Recent Analysis History</h3>
          <div className="overflow-x-auto scrollbar-hide">
            <div className="inline-block min-w-full align-middle">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Attack Type</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider hidden sm:table-cell">Hash Type</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Status</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider hidden md:table-cell">Risk Score</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider hidden lg:table-cell">Attempts</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {history.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900 capitalize">
                        {item.attack_type.replace('_', ' ')}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-600 hidden sm:table-cell">
                        {item.hash_type}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        {item.cracked ? (
                          <span className="badge-danger">Cracked</span>
                        ) : (
                          <span className="badge-success">Secure</span>
                        )}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-600 hidden md:table-cell">
                        <span className={`badge ${getRiskBadge(item.risk_score)}`}>
                          {item.risk_score.toFixed(1)}
                        </span>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-600 hidden lg:table-cell">
                        {item.attempts}
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

export default PasswordSimulator
