import Sidebar from '../components/Sidebar';
import { Outlet } from 'react-router-dom';

export default function MainLayout({ children }) {
  return (
    <div className="flex h-screen bg-indigo-50">
      <Sidebar />
      <main className="flex-1 min-w-0 p-6 overflow-y-auto bg-white h-screen">
        <Outlet />
      </main>
    </div>
  );
}
