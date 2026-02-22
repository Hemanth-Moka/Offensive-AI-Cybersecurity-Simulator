import React, { useState, useEffect } from 'react'
import { passwordAPI } from '../services/api'
import toast from 'react-hot-toast'
import { 
  HiOutlineLockClosed, HiOutlineKey, HiOutlineShieldCheck, 
  HiOutlineExclamationCircle, HiOutlineInformationCircle, 
  HiOutlineRefresh, HiOutlineCog, HiOutlineChartBar,
  HiOutlineClock, HiOutlineLightningBolt, HiOutlineCheckCircle,
  HiOutlineXCircle, HiOutlineDownload
} from 'react-icons/hi'

const PasswordSimulator = () => {
  const [formData, setFormData] = useState({
    password: '',
    hashType: 'MD5',
    attackType: 'dictionary',
    userMetadata: { name: '', dob: '' },
    maxAttempts: '',
    maxLength: 4,
    charset: 'lowercase+digits',
    userId: '',
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState([])
  const [showMetadata, setShowMetadata] = useState(false)
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [activeTab, setActiveTab] = useState('analyze')
  const [attackProgress, setAttackProgress] = useState(null)
  const [stats, setStats] = useState(null)

  useEffect(() => {
    loadHistory()
    loadStats()
    
    const interval = setInterval(() => {
      loadHistory()
      loadStats()
    }, 10000)

    return () => clearInterval(interval)
  }, [])

  const loadHistory = async () => {
    try {
      const response = await passwordAPI.getHistory(20)
      setHistory(response.data)
    } catch (error) {
      console.error('Failed to load history:', error)
    }
  }

  const loadStats = async () => {
    try {
      const response = await passwordAPI.getStats()
      setStats(response.data)
    } catch (error) {
      console.error('Failed to load stats:', error)
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
    setAttackProgress({ current: 0, total: 100, status: 'Starting attack...' })

    try {
      // Simulate progress for better UX
      const progressInterval = setInterval(() => {
        setAttackProgress(prev => {
          if (!prev) return null
          const newCurrent = Math.min(prev.current + Math.random() * 10, 95)
          return { ...prev, current: newCurrent, status: 'Testing passwords...' }
        })
      }, 200)

      const response = await passwordAPI.analyze({
        password: formData.password,
        hash_type: formData.hashType,
        attack_type: formData.attackType,
        user_metadata: showMetadata && (formData.userMetadata.name || formData.userMetadata.dob)
          ? formData.userMetadata
          : null,
        user_id: formData.userId || null,
        max_attempts: formData.maxAttempts ? parseInt(formData.maxAttempts) : null,
        max_length: formData.maxLength,
        charset: formData.charset,
      })

      clearInterval(progressInterval)
      setAttackProgress({ current: 100, total: 100, status: 'Complete!' })

      setResult(response.data)
      toast.success('Password analysis complete!')
      loadHistory()
      loadStats()
      
      setTimeout(() => {
        setAttackProgress(null)
        document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 500)
    } catch (error) {
      setAttackProgress(null)
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
    setAttackProgress({ current: 0, total: 100, status: 'Starting hash cracking...' })

    const hashType = e.target.hashType.value
    const attackType = e.target.attackType.value
    const maxAttempts = e.target.maxAttempts?.value ? parseInt(e.target.maxAttempts.value) : null
    const maxLength = e.target.maxLength?.value ? parseInt(e.target.maxLength.value) : 4
    const charset = e.target.charset?.value || 'lowercase+digits'

    try {
      const progressInterval = setInterval(() => {
        setAttackProgress(prev => {
          if (!prev) return null
          const newCurrent = Math.min(prev.current + Math.random() * 10, 95)
          return { ...prev, current: newCurrent, status: 'Cracking hash...' }
        })
      }, 200)

      const response = await passwordAPI.crackHash({
        hash_value: hashValue,
        hash_type: hashType,
        attack_type: attackType,
        user_metadata: null,
        max_attempts: maxAttempts,
        max_length: maxLength,
        charset: charset,
      })

      clearInterval(progressInterval)
      setAttackProgress({ current: 100, total: 100, status: 'Complete!' })

      setResult(response.data)
      toast.success('Hash analysis complete!')
      loadHistory()
      loadStats()
      
      setTimeout(() => {
        setAttackProgress(null)
        document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 500)
    } catch (error) {
      setAttackProgress(null)
      toast.error(error.response?.data?.detail || 'Hash cracking failed')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const exportResults = () => {
    if (!result) return
    
    const data = {
      timestamp: new Date().toISOString(),
      attack_type: result.attack_type,
      hash_type: formData.hashType,
      result: result,
    }
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `password-attack-${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
    toast.success('Results exported!')
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

  const formatTime = (seconds) => {
    if (seconds < 1) return `${(seconds * 1000).toFixed(2)} ms`
    if (seconds < 60) return `${seconds.toFixed(2)} seconds`
    const mins = Math.floor(seconds / 60)
    const secs = (seconds % 60).toFixed(2)
    return `${mins}m ${secs}s`
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
              Professional-grade password attack simulation with AI-powered pattern recognition, multiple attack vectors, and comprehensive security analysis.
            </p>
          </div>
          
          {/* Quick Stats */}
          {stats && (
            <div className="flex flex-wrap gap-3">
              <div className="bg-blue-50 px-4 py-2 rounded-lg border border-blue-200">
                <p className="text-xs text-gray-600">Total Attacks</p>
                <p className="text-lg font-bold text-blue-700">{stats.total_attacks}</p>
              </div>
              <div className="bg-green-50 px-4 py-2 rounded-lg border border-green-200">
                <p className="text-xs text-gray-600">Success Rate</p>
                <p className="text-lg font-bold text-green-700">{stats.success_rate}%</p>
              </div>
            </div>
          )}
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
            <HiOutlineKey className="inline mr-2" size={16} />
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
            <HiOutlineLockClosed className="inline mr-2" size={16} />
            Crack Hash
          </button>
        </div>

        {/* Attack Progress */}
        {attackProgress && (
          <div className="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-blue-900">{attackProgress.status}</span>
              <span className="text-sm text-blue-700">{Math.round(attackProgress.current)}%</span>
            </div>
            <div className="w-full bg-blue-200 rounded-full h-2.5">
              <div
                className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                style={{ width: `${attackProgress.current}%` }}
              ></div>
            </div>
          </div>
        )}

        {/* Forms */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Password Analysis Form */}
          {activeTab === 'analyze' && (
            <div className="lg:col-span-2">
              <form onSubmit={handleSubmit} className="space-y-5">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="sm:col-span-2">
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Password to Analyze <span className="text-red-500">*</span>
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
                    <p className="text-xs text-gray-500 mt-1">Password will be hashed and analyzed for vulnerabilities</p>
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
                      <option value="MD5">MD5 (Fast, Insecure)</option>
                      <option value="SHA256">SHA256 (Secure)</option>
                      <option value="bcrypt">bcrypt (Very Secure)</option>
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
                      <option value="brute_force">Brute Force Attack</option>
                      <option value="hybrid">Hybrid Attack</option>
                      <option value="ai_guided">AI-Guided Attack</option>
                    </select>
                  </div>
                </div>

                {/* Advanced Options */}
                <div className="border-t border-gray-200 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowAdvanced(!showAdvanced)}
                    className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center mb-3"
                  >
                    <HiOutlineCog className="mr-1" size={16} />
                    {showAdvanced ? 'Hide' : 'Show'} Advanced Options
                  </button>
                  {showAdvanced && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
                      <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">
                          Max Attempts (Optional)
                        </label>
                        <input
                          type="number"
                          value={formData.maxAttempts}
                          onChange={(e) => setFormData({ ...formData, maxAttempts: e.target.value })}
                          className="input-field text-sm"
                          placeholder="Unlimited"
                          min="1"
                        />
                      </div>
                      {formData.attackType === 'brute_force' && (
                        <>
                          <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">
                              Max Length
                            </label>
                            <input
                              type="number"
                              value={formData.maxLength}
                              onChange={(e) => setFormData({ ...formData, maxLength: parseInt(e.target.value) || 4 })}
                              className="input-field text-sm"
                              min="1"
                              max="6"
                            />
                          </div>
                          <div>
                            <label className="block text-xs font-medium text-gray-700 mb-1">
                              Character Set
                            </label>
                            <select
                              value={formData.charset}
                              onChange={(e) => setFormData({ ...formData, charset: e.target.value })}
                              className="input-field text-sm"
                            >
                              <option value="lowercase">Lowercase Only</option>
                              <option value="uppercase">Uppercase Only</option>
                              <option value="digits">Digits Only</option>
                              <option value="lowercase+digits">Lowercase + Digits</option>
                              <option value="uppercase+digits">Uppercase + Digits</option>
                              <option value="mixed">Mixed (Letters + Digits)</option>
                              <option value="full">Full (All Characters)</option>
                            </select>
                          </div>
                        </>
                      )}
                      <div>
                        <label className="block text-xs font-medium text-gray-700 mb-1">
                          User ID (for AI learning)
                        </label>
                        <input
                          type="text"
                          value={formData.userId}
                          onChange={(e) => setFormData({ ...formData, userId: e.target.value })}
                          className="input-field text-sm"
                          placeholder="Optional"
                        />
                      </div>
                    </div>
                  )}
                </div>

                {/* User Metadata */}
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
                    <>
                      <HiOutlineLightningBolt className="inline mr-2" size={18} />
                      Launch Attack
                    </>
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
                      Hash Value <span className="text-red-500">*</span>
                    </label>
                    <textarea
                      name="hash"
                      rows="3"
                      className="input-field font-mono text-sm"
                      placeholder="Enter hash value to crack (e.g., 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8)"
                      required
                    />
                    <p className="text-xs text-gray-500 mt-1">Paste the hash value you want to crack</p>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Hash Algorithm
                    </label>
                    <select name="hashType" className="input-field" defaultValue="MD5">
                      <option value="MD5">MD5</option>
                      <option value="SHA256">SHA256</option>
                      <option value="bcrypt">bcrypt</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Attack Type
                    </label>
                    <select name="attackType" className="input-field" defaultValue="dictionary">
                      <option value="dictionary">Dictionary Attack</option>
                      <option value="brute_force">Brute Force Attack</option>
                      <option value="hybrid">Hybrid Attack</option>
                      <option value="ai_guided">AI-Guided Attack</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Max Attempts (Optional)
                    </label>
                    <input
                      type="number"
                      name="maxAttempts"
                      className="input-field"
                      placeholder="Unlimited"
                      min="1"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Max Length (Brute Force)
                    </label>
                    <input
                      type="number"
                      name="maxLength"
                      className="input-field"
                      defaultValue="4"
                      min="1"
                      max="6"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                      Character Set (Brute Force)
                    </label>
                    <select name="charset" className="input-field" defaultValue="lowercase+digits">
                      <option value="lowercase">Lowercase Only</option>
                      <option value="uppercase">Uppercase Only</option>
                      <option value="digits">Digits Only</option>
                      <option value="lowercase+digits">Lowercase + Digits</option>
                      <option value="uppercase+digits">Uppercase + Digits</option>
                      <option value="mixed">Mixed (Letters + Digits)</option>
                      <option value="full">Full (All Characters)</option>
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
                    <>
                      <HiOutlineLockClosed className="inline mr-2" size={18} />
                      Crack Hash
                    </>
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
              Attack Results
            </h3>
            <div className="flex items-center gap-3">
              <span className={`badge ${getRiskBadge(result.overall_risk.overall_risk)}`}>
                {getRiskLabel(result.overall_risk.overall_risk)} Risk
              </span>
              <button
                onClick={exportResults}
                className="flex items-center gap-2 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium"
                title="Export results"
              >
                <HiOutlineDownload size={16} />
                Export
              </button>
            </div>
          </div>
          
          {/* Result Status */}
          <div className={`mb-6 p-4 rounded-lg border-2 ${
            result.cracked 
              ? 'bg-red-50 border-red-200' 
              : 'bg-green-50 border-green-200'
          }`}>
            <div className="flex items-center gap-3">
              {result.cracked ? (
                <>
                  <HiOutlineXCircle className="text-red-600" size={24} />
                  <div>
                    <p className="font-bold text-red-900">Password Cracked Successfully!</p>
                    <p className="text-sm text-red-700 mt-1">
                      The password was cracked in {result.attempts} attempt(s) using {result.attack_type.replace('_', ' ')} attack.
                    </p>
                  </div>
                </>
              ) : (
                <>
                  <HiOutlineCheckCircle className="text-green-600" size={24} />
                  <div>
                    <p className="font-bold text-green-900">Password Not Cracked</p>
                    <p className="text-sm text-green-700 mt-1">
                      The password resisted {result.attempts} attempt(s) using {result.attack_type.replace('_', ' ')} attack.
                    </p>
                  </div>
                </>
              )}
            </div>
            {result.cracked && (
              <div className="mt-4 p-3 bg-white rounded border border-red-300">
                <p className="text-xs font-semibold text-gray-600 mb-1">Cracked Password:</p>
                <p className="text-lg font-mono font-bold text-red-700 break-all">{result.cracked}</p>
              </div>
            )}
          </div>
          
          {/* Key Metrics Grid */}
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
              <p className="text-xs font-medium text-gray-600 mb-1 flex items-center">
                <HiOutlineClock className="mr-1" size={14} />
                Time Taken
              </p>
              <p className="text-lg sm:text-xl font-bold text-gray-900">
                {formatTime(result.time_taken)}
              </p>
              {result.attempts_per_second && (
                <p className="text-xs text-gray-500 mt-1">
                  {result.attempts_per_second.toLocaleString()} attempts/sec
                </p>
              )}
            </div>

            <div className="card bg-purple-50 border-purple-200">
              <p className="text-xs font-medium text-gray-600 mb-1 flex items-center">
                <HiOutlineChartBar className="mr-1" size={14} />
                Attempts
              </p>
              <p className="text-lg sm:text-xl font-bold text-gray-900">
                {result.attempts.toLocaleString()}
              </p>
              {result.total_attempts && (
                <p className="text-xs text-gray-500 mt-1">
                  of {result.total_attempts.toLocaleString()} total
                </p>
              )}
            </div>
          </div>

          {/* Pattern Analysis */}
          {result.pattern_analysis && Object.keys(result.pattern_analysis).length > 0 && (
            <div className="mb-6 card bg-gradient-to-r from-indigo-50 to-purple-50 border-indigo-200">
              <h4 className="text-lg font-bold text-gray-900 mb-3">Pattern Analysis</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white p-3 rounded-lg border border-indigo-200">
                  <p className="text-xs font-medium text-gray-600 mb-1">Strength Score</p>
                  <p className="text-2xl font-bold text-indigo-700">
                    {result.pattern_analysis.strength_score || 0}/100
                  </p>
                </div>
                <div className="bg-white p-3 rounded-lg border border-indigo-200">
                  <p className="text-xs font-medium text-gray-600 mb-1">Length</p>
                  <p className="text-2xl font-bold text-indigo-700">
                    {result.pattern_analysis.length || 0} chars
                  </p>
                </div>
                <div className="bg-white p-3 rounded-lg border border-indigo-200">
                  <p className="text-xs font-medium text-gray-600 mb-1">Complexity</p>
                  <p className="text-2xl font-bold text-indigo-700">
                    {result.pattern_analysis.complexity || 0}/4
                  </p>
                </div>
                <div className="bg-white p-3 rounded-lg border border-indigo-200">
                  <p className="text-xs font-medium text-gray-600 mb-1">Patterns Found</p>
                  <p className="text-lg font-bold text-indigo-700">
                    {result.pattern_analysis.patterns_found?.length || 0}
                  </p>
                </div>
              </div>
              
              {result.pattern_analysis.patterns_found && result.pattern_analysis.patterns_found.length > 0 && (
                <div className="mt-4">
                  <p className="text-sm font-semibold text-gray-700 mb-2">Detected Patterns:</p>
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

          {/* Risk Factors & Recommendations */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card bg-yellow-50 border-yellow-200">
              <h4 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                <HiOutlineExclamationCircle className="mr-2 text-yellow-600" size={20} />
                Risk Factors
              </h4>
              {result.overall_risk.factors && result.overall_risk.factors.length > 0 ? (
                <ul className="space-y-2">
                  {result.overall_risk.factors.map((factor, idx) => (
                    <li key={idx} className="flex items-start text-sm text-gray-700">
                      <span className="text-yellow-600 mr-2 font-bold">•</span>
                      <span>{factor}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-gray-600">No significant risk factors detected.</p>
              )}
            </div>

            <div className="card bg-blue-50 border-blue-200">
              <h4 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                <HiOutlineInformationCircle className="mr-2 text-blue-600" size={20} />
                Recommendations
              </h4>
              {result.overall_risk.recommendations && result.overall_risk.recommendations.length > 0 ? (
                <ul className="space-y-2">
                  {result.overall_risk.recommendations.map((rec, idx) => (
                    <li key={idx} className="flex items-start text-sm text-gray-700">
                      <span className="text-blue-600 mr-2 font-bold">•</span>
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-gray-600">Password appears secure. Maintain current practices.</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* History Section */}
      {history.length > 0 && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl sm:text-2xl font-bold text-gray-900">Recent Attack History</h3>
            <button
              onClick={loadHistory}
              className="flex items-center gap-2 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium"
              title="Refresh history"
            >
              <HiOutlineRefresh size={16} />
              Refresh
            </button>
          </div>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Attack Type</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden sm:table-cell">Hash Type</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden md:table-cell">Risk Score</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden lg:table-cell">Attempts</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {history.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
                      {item.created_at ? new Date(item.created_at).toLocaleString() : 'N/A'}
                    </td>
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
                      {item.attempts.toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default PasswordSimulator
