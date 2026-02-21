import React from 'react'
import { HiOutlineShieldCheck, HiOutlineDocumentText, HiOutlineInformationCircle } from 'react-icons/hi'

const Footer = () => {
  return (
    <footer className="bg-gradient-to-r from-gray-900 to-gray-800 text-white mt-16 border-t border-gray-700">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="text-lg font-bold mb-4 flex items-center">
              <HiOutlineShieldCheck className="mr-2 text-blue-400" size={20} />
              About
            </h3>
            <p className="text-sm text-gray-400 leading-relaxed">
              An AI-powered cybersecurity platform for ethical red-team awareness training. 
              Simulate password attacks and social engineering campaigns in a controlled environment.
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-bold mb-4 flex items-center">
              <HiOutlineDocumentText className="mr-2 text-blue-400" size={20} />
              Resources
            </h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
              <li><a href="#" className="hover:text-white transition-colors">API Reference</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Security Guidelines</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Best Practices</a></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-bold mb-4 flex items-center">
              <HiOutlineInformationCircle className="mr-2 text-blue-400" size={20} />
              Legal
            </h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Ethical Guidelines</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Disclaimer</a></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-700 pt-6">
          <div className="flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0">
            <div className="text-sm text-gray-400">
              <p>© {new Date().getFullYear()} Offensive AI - Cybersecurity Simulator</p>
              <p className="text-xs text-gray-500 mt-1">Educational Use Only - Controlled Lab Environment</p>
            </div>
            <div className="flex items-center space-x-2 text-xs text-gray-500">
              <span>Built by</span>
              <span className="text-red-500">Hemanth Moka</span>
              <span>for Security Education</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
