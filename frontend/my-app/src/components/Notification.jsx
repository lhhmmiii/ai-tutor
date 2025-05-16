import { useEffect } from 'react'

const icons = {
  success: (
    <svg className="w-6 h-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
    </svg>
  ),
  error: (
    <svg className="w-6 h-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
    </svg>
  ),
  info: (
    <svg className="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01" />
    </svg>
  )
}

const bgColors = {
  success: 'bg-green-50 border-green-200',
  error: 'bg-red-50 border-red-200',
  info: 'bg-blue-50 border-blue-200'
}

export default function Notification({ type = 'info', message, onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 3000)
    return () => clearTimeout(timer)
  }, [onClose])

  return (
    <div
      className={`fixed top-6 right-6 z-50 border shadow-md rounded-lg px-5 py-4 flex items-start space-x-3 animate-slide-in transition-all duration-300 ${bgColors[type]}`}
    >
      <div>{icons[type]}</div>
      <div className="text-sm font-medium text-gray-800">{message}</div>
      <button
        className="ml-4 text-gray-400 hover:text-gray-600 text-lg font-bold"
        onClick={onClose}
        aria-label="Close notification"
      >
        &times;
      </button>
    </div>
  )
}
