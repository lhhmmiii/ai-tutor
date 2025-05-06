import { useState, useEffect, useRef, use } from 'react'
import { WritingAgent } from '../services/writing_service'

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hi! Ask me about any vocabulary word.' },
  ])
  const [input, setInput] = useState('')
  const messagesEndRef = useRef(null)

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, isOpen])

  const sendMessage = async () => {
    if (!input.trim()) return
    const userMsg = { sender: 'user', text: input }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    const user_id = localStorage.getItem('user_id');
    try {
      const botResponse = await WritingAgent(user_id, input)
      const botMsg = {
        sender: 'bot',
        text: botResponse || "Sorry, I couldn't understand that.",
      }
  
      setMessages((prev) => [...prev, botMsg])
    } catch (error) {
      const errorMsg = {
        sender: 'bot',
        text: 'There was an error processing your request.',
      }
      setMessages((prev) => [...prev, errorMsg])
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
        <div className="fixed bottom-20 right-6 z-50 flex flex-col w-80 max-h-[500px] bg-indigo-700 rounded-lg shadow-lg overflow-hidden">
          <header className="flex items-center justify-between p-4 bg-indigo-900">
            <h3 className="text-white font-bold text-lg">Vocabulary Chatbot</h3>
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
                <p
                  className={`max-w-xs px-4 py-2 rounded-lg ${
                    msg.sender === 'user'
                      ? 'bg-indigo-500'
                      : 'bg-indigo-900 text-indigo-200 shadow'
                  }`}
                >
                  {msg.text}
                </p>
              </div>
            ))}
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
            />
            <button
              type="submit"
              className="bg-indigo-600 px-4 rounded hover:bg-indigo-700 text-white font-semibold disabled:opacity-50"
              disabled={!input.trim()}
            >
              Send
            </button>
          </form>
        </div>
      )}
    </>
  )
}
