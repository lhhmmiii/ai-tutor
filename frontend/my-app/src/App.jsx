import Sidebar from './components/Sidebar'
import AppRoutes from './routes/AppRoutes'

function App() {
  return (
    <div className="flex h-screen bg-indigo-50">
      <Sidebar />
      <main className="flex-1 min-w-0 p-6 overflow-y-auto bg-white h-screen">
        <AppRoutes />
      </main>
    </div>
  )
}

export default App
