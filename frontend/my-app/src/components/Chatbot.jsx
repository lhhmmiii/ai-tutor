import { useState, useEffect, useRef } from 'react'
import { WritingAgent } from '../services/writing_service'

// Loading animation component
const LoadingDots = () => (
  <div className="flex space-x-1">
    <div className="w-2 h-2 bg-indigo-300 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
    <div className="w-2 h-2 bg-indigo-300 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
    <div className="w-2 h-2 bg-indigo-300 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
  </div>
)

// Component to render different types of messages
const MessageContent = ({ content, type, style }) => {
  // Function to preserve line breaks and formatting
  const formatContent = (text) => {
    if (!text) return '';
    return text.split('\n').map((line, i) => (
      <span key={i}>
        {line}
        <br />
      </span>
    ));
  };

  switch (type) {
    case 'code':
      return (
        <pre className="bg-gray-800 p-4 rounded-lg overflow-x-auto whitespace-pre-wrap">
          <code className="text-gray-200">{content}</code>
        </pre>
      )
    case 'error':
      return (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded whitespace-pre-wrap">
          {formatContent(content)}
        </div>
      )
    case 'success':
      return (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded whitespace-pre-wrap">
          {formatContent(content)}
        </div>
      )
    default:
      return (
        <div className="whitespace-pre-wrap">
          {formatContent(content)}
        </div>
      )
  }
}

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([
    { 
      sender: 'bot', 
      content: 'Hi! How can I help you today?',
      type: 'text'
    },
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, isOpen])

  const parseBotResponse = (response) => {
    try {
      // Try to parse as JSON first
      const parsed = JSON.parse(response)
      
      // Handle different types of structured responses
      if (parsed.type === 'code') {
        return {
          content: parsed.content,
          type: 'code',
          language: parsed.language
        }
      } else if (parsed.type === 'error') {
        return {
          content: parsed.content,
          type: 'error'
        }
      } else if (parsed.type === 'success') {
        return {
          content: parsed.content,
          type: 'success'
        }
      } else if (Array.isArray(parsed)) {
        // Handle array of messages
        return {
          content: parsed.map(msg => msg.content || msg).join('\n'),
          type: 'text'
        }
      } else if (typeof parsed === 'object') {
        // Handle object with content
        return {
          content: parsed.content || JSON.stringify(parsed, null, 2),
          type: 'text'
        }
      }
      return parsed
    } catch (e) {
      // If not JSON, check if it contains code blocks or special formatting
      if (response.includes('```')) {
        // Handle markdown-style code blocks
        const parts = response.split('```')
        if (parts.length >= 3) {
          return {
            content: parts[1].trim(),
            type: 'code',
            language: parts[0].trim() || 'text'
          }
        }
      }
      
      // Return as regular text, preserving line breaks
      return {
        content: response,
        type: 'text'
      }
    }
  }

  const sendMessage = async () => {
    if (!input.trim()) return
    const userMsg = { 
      sender: 'user', 
      content: input,
      type: 'text'
    }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setIsLoading(true)
    
    const user_id = localStorage.getItem('user_id')
    try {
      const botResponse = await WritingAgent(user_id, input)
      console.log('Bot Response:', botResponse)
      
      const parsedResponse = parseBotResponse(botResponse)
      const botMsg = {
        sender: 'bot',
        ...parsedResponse
      }
  
      setMessages((prev) => [...prev, botMsg])
    } catch (error) {
      console.error('Error:', error)
      const errorMsg = {
        sender: 'bot',
        content: 'There was an error processing your request.',
        type: 'error'
      }
      setMessages((prev) => [...prev, errorMsg])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      {/* Icon chatbot nhỏ ở góc phải dưới màn hình */}
      <button
        aria-label="Open chatbot"
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 z-50 flex items-center justify-center w-14 h-14 rounded-full bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
      >
        {/* Bạn có thể thay icon bằng SVG */}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="w-7 h-7"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M8 10h.01M12 10h.01M16 10h.01M9 16h6m2 4H7a2 2 0 01-2-2V7a2 2 0 012-2h10a2 2 0 012 2v11a2 2 0 01-2 2z"
          />
        </svg>
      </button>

      {/* Popup chatbox */}
      {isOpen && (
        <div className="fixed bottom-20 right-6 z-50 flex flex-col w-96 max-h-[600px] bg-indigo-700 rounded-lg shadow-lg overflow-hidden">
          <header className="flex items-center justify-between p-4 bg-indigo-900">
            <h3 className="text-white font-bold text-lg">LHH</h3>
            <button
              aria-label="Close chatbot"
              onClick={() => setIsOpen(false)}
              className="text-indigo-300 hover:text-white focus:outline-none"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="w-6 h-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </header>

          <div
            className="flex-1 p-4 overflow-y-auto space-y-3 bg-indigo-800 text-white"
            aria-live="polite"
          >
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex ${
                  msg.sender === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-xs px-4 py-2 rounded-lg ${
                    msg.sender === 'user'
                      ? 'bg-indigo-500'
                      : 'bg-indigo-900 text-indigo-200 shadow'
                  }`}
                >
                  <MessageContent 
                    content={msg.content} 
                    type={msg.type}
                    style={msg.style}
                  />
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="max-w-xs px-4 py-2 rounded-lg bg-indigo-900 text-indigo-200 shadow">
                  <LoadingDots />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form
            onSubmit={(e) => {
              e.preventDefault()
              sendMessage()
            }}
            className="flex p-3 gap-2 bg-indigo-900"
          >
            <input
              type="text"
              className="flex-grow rounded px-3 py-2 text-indigo-900"
              placeholder="Ask me about a word..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              aria-label="Chat input"
              disabled={isLoading}
            />
            <button
              type="submit"
              className="bg-indigo-600 px-4 rounded hover:bg-indigo-700 text-white font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={!input.trim() || isLoading}
            >
              {isLoading ? (
                <div className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Sending...
                </div>
              ) : (
                'Send'
              )}
            </button>
          </form>
        </div>
      )}
    </>
  )
}
