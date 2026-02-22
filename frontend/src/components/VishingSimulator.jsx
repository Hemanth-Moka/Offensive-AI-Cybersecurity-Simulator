import React, { useState, useEffect } from 'react'
import { vishingAPI } from '../services/api'
import toast from 'react-hot-toast'
import { HiOutlinePhone, HiOutlineExclamationCircle, HiOutlineInformationCircle, HiOutlineShieldCheck, HiOutlineRefresh } from 'react-icons/hi'

const VishingSimulator = () => {
  const [formData, setFormData] = useState({
    callScript: '',
    callerId: '',
    callDuration: 0,
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [loadingTranscription, setLoadingTranscription] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
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
      const response = await vishingAPI.getHistory(10)
      setHistory(response.data)
    } catch (error) {
      console.error('Failed to load history:', error)
    }
  }

  const handleFileSelect = (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    const validFormats = ['audio/mpeg', 'audio/wav', 'audio/mp4', 'audio/x-wav']
    const validExtensions = ['.mp3', '.wav', '.m4a']
    const fileName = file.name.toLowerCase()
    
    const hasValidExtension = validExtensions.some(ext => fileName.endsWith(ext))
    const hasValidMimetype = validFormats.includes(file.type) || file.type === 'audio/m4a'

    if (!hasValidExtension && !hasValidMimetype) {
      toast.error('Invalid format. Please upload mp3, wav, or m4a files.')
      e.target.value = ''
      return
    }

    if (file.size > 50 * 1024 * 1024) {
      toast.error('File size exceeds 50MB limit')
      e.target.value = ''
      return
    }

    setSelectedFile(file)
  }

  const handleTranscribe = async (e) => {
    e.preventDefault()
    if (!selectedFile) {
      toast.error('Please select an audio file to transcribe')
      return
    }

    setLoadingTranscription(true)
    try {
      const formData = new FormData()
      formData.append('audio_file', selectedFile)

      const response = await vishingAPI.transcribe(formData)
      
      if (response.data?.transcript) {
        setFormData(prev => ({
          ...prev,
          callScript: response.data.transcript
        }))
        toast.success('Transcription complete! Ready to analyze.')
        setSelectedFile(null)
        if (document.getElementById('audio-input')) {
          document.getElementById('audio-input').value = ''
        }
      } else {
        toast.error('No transcript returned from server')
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 
                          error.response?.data?.message || 
                          'Transcription failed'
      toast.error(errorMessage)
      console.error('Transcription error:', error)
    } finally {
      setLoadingTranscription(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.callScript.trim()) {
      toast.error('Please enter a call script')
      return
    }
    
    setLoading(true)
    setResult(null)

    try {
      const response = await vishingAPI.analyze({
        call_script: formData.callScript,
        caller_id: formData.callerId,
        call_duration: formData.callDuration,
      })

      setResult(response.data)
      toast.success('Vishing analysis complete!')
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

  const loadSampleCall = (type) => {
    const samples = {
      vishing: {
        script: 'Hello, this is Officer Smith calling from the Internal Revenue Service. We have detected fraudulent activity on your Social Security number and tax account. Your account has been suspended and legal action will be taken if you do not verify your identity immediately. Please provide your full Social Security number, date of birth, and bank account information to resolve this urgent matter right now.',
        callerId: '+1-800-555-0199',
        duration: 180,
      },
      legitimate: {
        script: 'Hello, this is a courtesy call from your bank regarding your recent account activity. We noticed a transaction that may need your attention. If you would like to discuss this, please call us back at the number on the back of your card during business hours. Thank you.',
        callerId: '1-800-BANK-123',
        duration: 45,
      },
    }

    setFormData({
      callScript: samples[type].script,
      callerId: samples[type].callerId,
      callDuration: samples[type].duration,
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
              <div className="p-2 bg-indigo-100 rounded-lg">
                <HiOutlinePhone className="text-indigo-600" size={24} />
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-gray-900">Voice Phishing (Vishing) Simulator</h2>
            </div>
            <p className="text-gray-600 mt-2 text-sm sm:text-base">
              Analyze voice call scripts for vishing indicators, social engineering tactics, and voice phishing attempts using advanced AI detection.
            </p>
          </div>
        </div>

        {/* Sample Call Buttons */}
        <div className="mb-6 flex flex-wrap gap-3">
          <button
            onClick={() => loadSampleCall('vishing')}
            className="btn-secondary bg-red-50 text-red-700 hover:bg-red-100 border-red-200"
          >
            Load Sample Vishing Call
          </button>
          <button
            onClick={() => loadSampleCall('legitimate')}
            className="btn-secondary bg-green-50 text-green-700 hover:bg-green-100 border-green-200"
          >
            Load Sample Legitimate Call
          </button>
        </div>

        {/* Voice Upload Section */}
        <div className="mb-6 card bg-indigo-50 border-indigo-200">
          <div className="flex items-start gap-4">
            <div className="flex-1">
              <h4 className="text-lg font-bold text-gray-900 mb-2">📞 Upload Call Recording</h4>
              <p className="text-sm text-gray-700 mb-4">
                Upload an audio file (mp3, wav, m4a) to automatically transcribe and analyze the call. Max 50MB.
              </p>
              <div className="flex flex-col sm:flex-row gap-3">
                <div className="flex-1">
                  <input
                    id="audio-input"
                    type="file"
                    accept=".mp3,.wav,.m4a,audio/mpeg,audio/wav,audio/mp4"
                    onChange={handleFileSelect}
                    disabled={loadingTranscription}
                    className="block w-full text-sm text-gray-500
                      file:mr-4 file:py-2 file:px-4
                      file:rounded-md file:border-0
                      file:text-sm file:font-semibold
                      file:bg-indigo-100 file:text-indigo-700
                      hover:file:bg-indigo-200
                      disabled:opacity-50 disabled:cursor-not-allowed
                      cursor-pointer"
                  />
                  {selectedFile && (
                    <p className="text-xs text-indigo-700 mt-2">
                      ✓ {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
                    </p>
                  )}
                </div>
                <button
                  onClick={handleTranscribe}
                  disabled={!selectedFile || loadingTranscription}
                  className="btn-secondary bg-indigo-100 text-indigo-700 hover:bg-indigo-200 border-indigo-300 disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
                >
                  {loadingTranscription ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-indigo-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Transcribing...
                    </span>
                  ) : (
                    'Transcribe Audio'
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Caller ID / Phone Number
              </label>
              <input
                type="text"
                value={formData.callerId}
                onChange={(e) => setFormData({ ...formData, callerId: e.target.value })}
                className="input-field"
                placeholder="+1-800-555-0199 or Unknown"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Call Duration (seconds)
              </label>
              <input
                type="number"
                value={formData.callDuration}
                onChange={(e) => setFormData({ ...formData, callDuration: parseFloat(e.target.value) || 0 })}
                className="input-field"
                placeholder="180"
                min="0"
                step="1"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Call Script / Transcript <span className="text-red-500">*</span>
            </label>
            <textarea
              value={formData.callScript}
              onChange={(e) => setFormData({ ...formData, callScript: e.target.value })}
              className="textarea-field"
              rows="10"
              placeholder="Enter the call script or transcript here..."
              required
            />
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
              'Analyze Call'
            )}
          </button>
        </form>
      </div>

      {/* Results Section */}
      {result && (
        <div id="results-section" className="card animate-slide-up">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
            <h3 className="text-xl sm:text-2xl font-bold text-gray-900 flex items-center mb-2 sm:mb-0">
              <HiOutlineShieldCheck className="mr-2 text-indigo-600" size={24} />
              Analysis Results
            </h3>
            <span className={`badge ${getRiskBadge(result.overall_risk.overall_risk)}`}>
              {getRiskLabel(result.overall_risk.overall_risk)}
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div className={`card border-2 ${getRiskColor(result.overall_risk.overall_risk)}`}>
              <p className="text-xs font-medium text-gray-600 mb-1">Vishing Risk</p>
              <p className="text-2xl sm:text-3xl font-bold">{getRiskLabel(result.overall_risk.overall_risk)}</p>
              <p className="text-xs text-gray-500 mt-1">Score: {result.overall_risk.overall_risk.toFixed(1)}/100</p>
            </div>

            <div className="card bg-gradient-to-br from-indigo-50 to-indigo-100 border-indigo-200">
              <p className="text-xs font-medium text-gray-600 mb-1">Success Rate</p>
              <p className="text-2xl sm:text-3xl font-bold text-gray-900">{result.success_rate_simulation.toFixed(1)}%</p>
              <p className="text-xs text-gray-500 mt-1">Estimated compliance</p>
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

          {result.social_engineering_tactics && result.social_engineering_tactics.length > 0 && (
            <div className="mb-6 card bg-red-50 border-red-200">
              <h4 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                <HiOutlineExclamationCircle className="mr-2 text-red-600" size={20} />
                Social Engineering Tactics Detected
              </h4>
              <div className="flex flex-wrap gap-2">
                {result.social_engineering_tactics.map((tactic, idx) => (
                  <span key={idx} className="badge-danger capitalize">
                    {tactic.replace('_', ' ')}
                  </span>
                ))}
              </div>
            </div>
          )}

          {result.suspicious_indicators && result.suspicious_indicators.length > 0 && (
            <div className="mb-6 card bg-yellow-50 border-yellow-200">
              <h4 className="text-lg font-bold text-gray-900 mb-3">Suspicious Indicators</h4>
              <ul className="space-y-2">
                {result.suspicious_indicators.map((indicator, idx) => (
                  <li key={idx} className="flex items-start text-sm text-gray-700">
                    <HiOutlineExclamationCircle className="mr-2 text-yellow-600 flex-shrink-0 mt-0.5" size={16} />
                    <span>{indicator}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {result.caller_analysis && (
            <div className="mb-6 card bg-gray-50">
              <h4 className="text-lg font-bold text-gray-900 mb-3">Caller Analysis</h4>
              <div className="space-y-2">
                <p className="text-sm text-gray-700">
                  <strong className="text-gray-900">Caller ID:</strong> {result.caller_analysis.caller_id || 'Not provided'}
                </p>
                <p className="text-sm text-gray-700">
                  <strong className="text-gray-900">Call Duration:</strong> {result.caller_analysis.call_duration} seconds
                </p>
                {result.caller_analysis.suspicious_caller && (
                  <div className="flex items-center text-sm text-red-600 bg-red-50 p-2 rounded-lg mt-2">
                    <HiOutlineExclamationCircle className="mr-2" size={16} />
                    ⚠️ Suspicious caller ID pattern detected
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
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Call Script</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider hidden sm:table-cell">Caller ID</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Risk</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider hidden md:table-cell">Success Rate</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {history.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 text-sm font-medium text-gray-900 max-w-xs truncate">
                        {item.call_script}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600 hidden sm:table-cell">
                        {item.caller_id || 'N/A'}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span className={`badge ${getRiskBadge(item.vishing_score)}`}>
                          {item.vishing_score.toFixed(1)}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600 hidden md:table-cell">
                        {item.success_rate_simulation.toFixed(1)}%
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

export default VishingSimulator
