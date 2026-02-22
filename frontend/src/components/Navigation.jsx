import React, { useState } from "react";
import { HiOutlineChartBar, HiOutlineLockClosed, HiOutlineMail, HiOutlinePhone, HiOutlineUser, HiMenu, HiX } from "react-icons/hi";
import { FaBrain } from "react-icons/fa";
import { FaExclamationTriangle } from "react-icons/fa";

const Navigation = ({ activeTab, setActiveTab }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const tabs = [
    { id: "dashboard", label: "Dashboard", icon: <HiOutlineChartBar size={20} />, shortLabel: "Dashboard" },
    { id: "password", label: "Password Simulator", icon: <HiOutlineLockClosed size={20} />, shortLabel: "Password" },
    { id: "phishing", label: "Phishing Simulator", icon: <HiOutlineMail size={20} />, shortLabel: "Phishing" },
    { id: "vishing", label: "Vishing Simulator", icon: <HiOutlinePhone size={20} />, shortLabel: "Vishing" },
    { id: "behavior", label: "User Behavior", icon: <HiOutlineUser size={20} />, shortLabel: "Behavior" },
  ];

  return (
    <nav className="bg-gradient-to-r from-gray-900 to-gray-800 text-white shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo Section */}
          <div className="flex items-center space-x-2 sm:space-x-3 flex-shrink-0">
            <div className="relative">
              <FaBrain size={28} className="text-blue-400 animate-pulse-slow" />
              <div className="absolute inset-0 "></div>
            </div>
            <div className="hidden sm:block">
              <h1 className="text-lg sm:text-xl font-bold bg-gradient-to-r from-blue-400 to-blue-300 bg-clip-text text-transparent">
                Offensive AI
              </h1>
              <p className="text-xs text-gray-400 hidden lg:block">Cybersecurity Simulator</p>
            </div>
          </div>

          {/* Desktop Tabs */}
          <div className="hidden md:flex items-center space-x-1 lg:space-x-2">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center px-3 lg:px-4 py-2 rounded-lg transition-all duration-200 ${
                  activeTab === tab.id
                    ? "bg-blue-600 text-white "
                    : "text-gray-300 hover:bg-gray-700 hover:text-white"
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                <span className="text-sm lg:text-base font-medium">{tab.label}</span>
              </button>
            ))}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-lg text-gray-300 hover:bg-gray-700 hover:text-white transition-colors"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <HiX size={24} /> : <HiMenu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-gray-800 border-t border-gray-700 animate-slide-up">
          <div className="px-4 py-2 space-y-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id);
                  setMobileMenuOpen(false);
                }}
                className={`w-full flex items-center px-4 py-3 rounded-lg transition-all duration-200 ${
                  activeTab === tab.id
                    ? "bg-blue-600 text-white shadow-lg"
                    : "text-gray-300 hover:bg-gray-700 hover:text-white"
                }`}
              >
                <span className="mr-3">{tab.icon}</span>
                <span className="font-medium">{tab.label}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Warning Bar */}
      <div className="bg-gradient-to-r from-yellow-500 to-yellow-500 text-white text-center py-2 px-4 text-xs sm:text-sm font-medium shadow-md">
        <span className="inline-flex items-center">
         <span className="mr-2 text-red-500 mb-0.5">
  <FaExclamationTriangle size={16} />
</span>
          Educational Use Only - Beta Version - Use in Controlled Lab Environment
        </span>
      </div>
    </nav>
  );
};

export default Navigation;