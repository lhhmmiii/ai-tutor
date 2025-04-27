import { Outlet } from 'react-router-dom';

export default function AuthLayout() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-indigo-50 p-6">
      <div className="w-full max-w-md">
        <Outlet />
      </div>
    </div>
  );
}
