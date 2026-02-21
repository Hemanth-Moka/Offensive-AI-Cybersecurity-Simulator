import React, { useEffect, useState } from "react"
import { passwordAPI, phishingAPI, vishingAPI } from "../services/api"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend,
} from "recharts"
import toast from "react-hot-toast"
import {
  HiOutlineShieldCheck,
  HiOutlineLockClosed,
  HiOutlineMail,
  HiOutlineExclamationCircle,
  HiOutlinePhone,
} from "react-icons/hi"

const Dashboard = () => {
  const [passwordStats, setPasswordStats] = useState(null)
  const [phishingStats, setPhishingStats] = useState(null)
  const [vishingStats, setVishingStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const [pwdStats, phishStats, vishStats] = await Promise.all([
        passwordAPI.getStats(),
        phishingAPI.getStats(),
        vishingAPI.getStats(),
      ])

      setPasswordStats(pwdStats.data)
      setPhishingStats(phishStats.data)
      setVishingStats(vishStats.data)
    } catch (error) {
      toast.error("Failed to load statistics")
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-10 w-10 border-4 border-gray-300 border-t-indigo-600"></div>
      </div>
    )
  }

  const passwordChartData = passwordStats?.attacks_by_type
    ? Object.entries(passwordStats.attacks_by_type).map(([type, count]) => ({
        name: type.replace("_", " ").toUpperCase(),
        count,
      }))
    : []

  const riskData = [
    { name: "Low", value: 30, color: "#16a34a" },
    { name: "Medium", value: 40, color: "#f59e0b" },
    { name: "High", value: 20, color: "#dc2626" },
    { name: "Critical", value: 10, color: "#7f1d1d" },
  ]

  return (
    <div className="min-h-screen bg-gray-50 px-8 py-8">
      {/* HEADER */}
      <div className="flex justify-between items-center mb-10">
        <div>
          <h1 className="text-3xl font-semibold text-gray-900">
            Security Operations Dashboard
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Enterprise simulation analytics overview
          </p>
        </div>

        <div className="bg-green-100 text-green-700 text-sm px-4 py-2 rounded-full font-medium">
          ● System Secure
        </div>
      </div>

      {/* KPI CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-5 gap-6 mb-10">
        <StatCard
          title="Password Attacks"
          value={passwordStats?.total_attacks || 0}
          icon={<HiOutlineLockClosed size={20} />}
        />
        <StatCard
          title="Cracked Passwords"
          value={passwordStats?.successful_cracks || 0}
          icon={<HiOutlineShieldCheck size={20} />}
        />
        <StatCard
          title="Emails Analyzed"
          value={phishingStats?.total_emails_analyzed || 0}
          icon={<HiOutlineMail size={20} />}
        />
        <StatCard
          title="High Risk Emails"
          value={phishingStats?.high_risk_emails || 0}
          icon={<HiOutlineExclamationCircle size={20} />}
        />
        <StatCard
          title="Calls Analyzed"
          value={vishingStats?.total_calls_analyzed || 0}
          icon={<HiOutlinePhone size={20} />}
        />
      </div>

      {/* CHARTS */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-10">
        <ChartCard title="Attack Type Distribution">
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={passwordChartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis />
              <Tooltip />
              <Bar
                dataKey="count"
                fill="#4f46e5"
                radius={[6, 6, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Risk Level Distribution">
          <ResponsiveContainer width="100%" height={350}>
            <PieChart>
              <Pie
                data={riskData}
                dataKey="value"
                outerRadius={110}
                label
              >
                {riskData.map((entry, index) => (
                  <Cell key={index} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* PERFORMANCE METRICS */}
      <div>
        <h2 className="text-lg font-semibold text-gray-800 mb-6">
          Performance Metrics
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <MetricCard
            title="Password Crack Rate"
            value={passwordStats?.success_rate || 0}
          />
          <MetricCard
            title="Average Password Risk"
            value={passwordStats?.average_risk_score || 0}
          />
          <MetricCard
            title="Average Phishing Score"
            value={phishingStats?.average_phishing_score || 0}
          />
          <MetricCard
            title="Average Click Rate"
            value={phishingStats?.average_click_rate || 0}
          />
          <MetricCard
            title="Vishing Success Rate"
            value={vishingStats?.average_success_rate || 0}
          />
          <MetricCard
            title="Average Vishing Score"
            value={vishingStats?.average_vishing_score || 0}
          />
        </div>
      </div>
    </div>
  )
}

/* COMPONENTS */

const StatCard = ({ title, value, icon }) => (
  <div className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm hover:shadow-md transition">
    <div className="flex justify-between items-center">
      <div>
        <p className="text-sm text-gray-500">{title}</p>
        <p className="text-2xl font-semibold text-gray-900 mt-1">{value}</p>
      </div>
      <div className="w-10 h-10 flex items-center justify-center rounded-lg bg-indigo-50 text-indigo-600">
        {icon}
      </div>
    </div>
  </div>
)

const ChartCard = ({ title, children }) => (
  <div className="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
    <h3 className="text-md font-semibold text-gray-800 mb-4">
      {title}
    </h3>
    {children}
  </div>
)

const MetricCard = ({ title, value }) => (
  <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
    <p className="text-sm text-gray-500 mb-3">{title}</p>
    <div className="flex items-center justify-between">
      <div className="w-full bg-gray-200 h-2 rounded-full mr-4">
        <div
          className="bg-indigo-600 h-2 rounded-full"
          style={{ width: `${value}%` }}
        />
      </div>
      <span className="text-sm font-semibold text-gray-800">
        {value.toFixed(1)}%
      </span>
    </div>
  </div>
)

export default Dashboard