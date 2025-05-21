import { useState, useRef, useEffect } from 'react'
import { ConversationAgent } from '../services/writing_service'

const dataMap = {
  'Ordering Food': {
    Student: ['Waiter'],
    Traveler: ['Waiter'],
    Tourist: ['Waiter'],
  },
  'Job Interview': {
    'Job Applicant': ['Interviewer'],
    'Intern': ['HR Manager'],
  },
  'Booking a Hotel': {
    Tourist: ['Receptionist'],
    Traveler: ['Hotel Manager'],
  },
  'Traveling Abroad': {
    Traveler: ['Customs Officer', 'Immigration Officer'],
    Student: ['Immigration Officer'],
  },
  'Visiting a Doctor': {
    Student: ['Doctor'],
    Worker: ['Doctor', 'Nurse'],
  },
  'Checking in at the Airport': {
    Traveler: ['Check-in Agent'],
    Tourist: ['Airline Staff'],
  },
  'Shopping at a Mall': {
    Student: ['Cashier'],
    Tourist: ['Store Assistant'],
  },
  'Making a Reservation': {
    Traveler: ['Receptionist'],
    Tourist: ['Booking Agent'],
  },
  'Asking for Directions': {
    Tourist: ['Local Resident'],
    Traveler: ['Police Officer'],
  },
  'Going to the Bank': {
    Worker: ['Bank Teller'],
    Student: ['Bank Clerk'],
  },
  'Buying Train Tickets': {
    Traveler: ['Ticket Seller'],
    Tourist: ['Station Assistant'],
  },
  'Renting a Car': {
    Tourist: ['Rental Agent'],
    Businessperson: ['Receptionist'],
  },
  'Meeting New People': {
    Student: ['Stranger'],
    Tourist: ['Local Resident'],
  },
  'Phone Call Support': {
    Worker: ['Customer Support Agent'],
    Student: ['Technical Support'],
  },
}


const LoadingDots = () => (
  <div className="flex space-x-1">
    <div className="w-2 h-2 bg-indigo-300 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
    <div className="w-2 h-2 bg-indigo-300 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
    <div className="w-2 h-2 bg-indigo-300 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
  </div>
)

const Message = ({ sender, content }) => {
  const baseStyle = 'max-w-xs px-4 py-2 rounded-lg shadow whitespace-pre-wrap'
  const userStyle = 'bg-indigo-500 text-white self-end'
  const botStyle = 'bg-indigo-900 text-indigo-200 self-start'
  const systemStyle = 'bg-gray-700 text-gray-200 self-center text-sm italic px-2 py-1 rounded'

  const style =
    sender === 'user'
      ? userStyle
      : sender === 'system'
      ? systemStyle
      : botStyle

  return <div className={`flex ${sender === 'user' ? 'justify-end' : 'justify-start'}`}>
    <div className={`${baseStyle} ${style}`}>{content}</div>
  </div>
}

export default function ConversationBot() {
  const [isOpen, setIsOpen] = useState(false)
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [messages, setMessages] = useState([])
  const [topic, setTopic] = useState('')
  const [userRole, setUserRole] = useState('')
  const [botRole, setBotRole] = useState('')
  const [started, setStarted] = useState(false)
  const messagesEndRef = useRef(null)

  const roleOptions = topic ? Object.keys(dataMap[topic] || {}) : []
  const botRoleOptions = topic && userRole ? (dataMap[topic]?.[userRole] || []) : []

  useEffect(() => {
    if (isOpen) messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isOpen])

  const startConversation = async () => {
    setStarted(true)
    const intro = `Let's begin a conversation.\nTopic: ${topic}.\nYou are a ${userRole}.\nI will be a ${botRole}.`
    setMessages([{ sender: 'system', content: intro }])

    try {
      const user_id = localStorage.getItem('user_id')
      const response = await ConversationAgent(user_id, intro)
      setMessages(prev => [...prev, { sender: 'bot', content: response }])
    } catch {
      setMessages(prev => [...prev, { sender: 'bot', content: 'Error starting conversation.' }])
    }
  }

  const sendMessage = async () => {
    if (!input.trim()) return
    const userMsg = { sender: 'user', content: input }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setIsLoading(true)

    try {
      const user_id = localStorage.getItem('user_id')
      const prompt = `Continue the roleplay.\nTopic: ${topic}.\nYou are a ${botRole}. The user is a ${userRole}.\nTheir message: "${input}"`
      const botResponse = await ConversationAgent(user_id, prompt)
      setMessages((prev) => [...prev, { sender: 'bot', content: botResponse }])
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'bot', content: 'An error occurred while responding.' }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg"
      >
        💬
      </button>

      {isOpen && (
        <div className="fixed bottom-20 right-6 z-50 w-96 max-h-[600px] bg-indigo-700 rounded-lg shadow-lg overflow-hidden flex flex-col">
          <header className="p-4 bg-indigo-900 text-white font-bold flex justify-between items-center">
            Conversation Practice
            <button onClick={() => setIsOpen(false)} className="text-indigo-300 hover:text-white">✖</button>
          </header>

          {!started ? (
            <div className="flex flex-col gap-3 p-4 bg-indigo-800 text-white">
              <label>
                Topic:
                <select
                  className="w-full mt-1 p-2 text-indigo-900 rounded"
                  value={topic}
                  onChange={e => {
                    setTopic(e.target.value)
                    setUserRole('')
                    setBotRole('')
                  }}
                >
                  <option value="">-- Select --</option>
                  {Object.keys(dataMap).map(t => <option key={t}>{t}</option>)}
                </select>
              </label>

              {topic && (
                <label>
                  Your Role:
                  <select
                    className="w-full mt-1 p-2 text-indigo-900 rounded"
                    value={userRole}
                    onChange={e => {
                      setUserRole(e.target.value)
                      setBotRole('')
                    }}
                  >
                    <option value="">-- Select --</option>
                    {roleOptions.map(r => <option key={r}>{r}</option>)}
                  </select>
                </label>
              )}

              {userRole && (
                <label>
                  Bot's Role:
                  <select
                    className="w-full mt-1 p-2 text-indigo-900 rounded"
                    value={botRole}
                    onChange={e => setBotRole(e.target.value)}
                  >
                    <option value="">-- Select --</option>
                    {botRoleOptions.map(b => <option key={b}>{b}</option>)}
                  </select>
                </label>
              )}

              <button
                disabled={!topic || !userRole || !botRole}
                onClick={startConversation}
                className="mt-2 px-4 py-2 bg-indigo-600 rounded hover:bg-indigo-700 font-semibold disabled:opacity-50"
              >
                Start Conversation
              </button>
            </div>
          ) : (
            <>
              <div className="flex-1 p-4 overflow-y-auto space-y-3 bg-indigo-800 text-white">
                {messages.map((msg, i) => <Message key={i} {...msg} />)}
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
                  placeholder="Say something..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  disabled={isLoading}
                />
                <button
                  type="submit"
                  disabled={!input.trim() || isLoading}
                  className="bg-indigo-600 px-4 rounded hover:bg-indigo-700 text-white font-semibold disabled:opacity-50"
                >
                  Send
                </button>
              </form>
            </>
          )}
        </div>
      )}
    </>
  )
}
