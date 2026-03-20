import React, { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import Dashboard from './components/Dashboard'
import { LayoutDashboard, MessageCircle } from 'lucide-react'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <nav className="bg-white border-b px-6 py-4 flex justify-between items-center shadow-sm">
        <div className="text-2xl font-black text-blue-600 flex items-center">
            📚 <span className="ml-2">AI COMPANION</span>
        </div>
        <div className="flex space-x-4 bg-gray-50 p-1 rounded-xl">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`flex items-center px-6 py-2 rounded-lg font-bold transition-all ${
              activeTab === 'dashboard'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-gray-500 hover:bg-gray-200'
            }`}
          >
            <LayoutDashboard className="mr-2" size={18} /> Dashboard
          </button>
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex items-center px-6 py-2 rounded-lg font-bold transition-all ${
              activeTab === 'chat'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-gray-500 hover:bg-gray-200'
            }`}
          >
            <MessageCircle className="mr-2" size={18} /> Chat with AI
          </button>
        </div>
      </nav>

      <main className="flex-1 overflow-hidden p-6">
        {activeTab === 'dashboard' ? (
          <Dashboard />
        ) : (
          <div className="flex items-center justify-center h-full">
            <ChatInterface />
          </div>
        )}
      </main>
    </div>
  )
}

export default App
