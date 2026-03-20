import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, User, Bot, Loader } from 'lucide-react';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { role: 'bot', content: "Hello! I'm your AI Study Companion. How can I help you today?" }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      // Try to get a valid topic ID
      let topicId = 1;
      try {
        const subjects = await axios.get('http://localhost:8000/subjects/');
        if (subjects.data.length > 0 && subjects.data[0].topics.length > 0) {
            topicId = subjects.data[0].topics[0].id;
        }
      } catch (e) {}

      // Call the new AI chat endpoint
      const response = await axios.post(`http://localhost:8000/ai/chat/?message=${encodeURIComponent(input)}&topic_id=${topicId}`);
      const botMessage = {
        role: 'bot',
        content: response.data.response
      };
      setMessages(prev => [...prev, botMessage]);

      // Randomly trigger a challenge
      if (Math.random() > 0.6) {
        setTimeout(async () => {
          setLoading(true);
          const challenge = await axios.get('http://localhost:8000/ai/challenge/');
          setMessages(prev => [...prev, {
            role: 'bot',
            content: `Actually, let's see how much you really know. ${challenge.data.question}`
          }]);
          setLoading(false);
        }, 1500);
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'bot', content: "I'm sorry, I'm having trouble connecting to the brain right now." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[500px] w-full max-w-2xl mx-auto border rounded-lg overflow-hidden bg-white shadow-lg">
      <div className="bg-blue-600 text-white p-4 font-bold flex items-center">
        <Bot className="mr-2" /> AI Study Companion
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 rounded-lg flex items-start ${
              m.role === 'user' ? 'bg-blue-100 text-blue-900' : 'bg-gray-100 text-gray-900'
            }`}>
              {m.role === 'user' ? <User size={18} className="mr-2 mt-1" /> : <Bot size={18} className="mr-2 mt-1" />}
              <div>{m.content}</div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 p-3 rounded-lg flex items-center">
              <Loader className="animate-spin mr-2" size={18} /> thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="p-4 border-t flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me anything about your studies..."
          className="flex-1 border rounded-l-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button type="submit" className="bg-blue-600 text-white p-2 rounded-r-lg hover:bg-blue-700">
          <Send size={20} />
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;
