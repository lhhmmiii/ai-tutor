import { Link, useLocation } from 'react-router-dom';
import { logout } from '../services/auth_service';
import { useNavigate } from 'react-router-dom';


function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();

  const links = [
    { name: 'Grammar Check', path: '/' },
    { name: 'Analyze Level', path: '/analyze' },
    { name: 'Writing Feedback', path: '/feedback' },
    { name: 'Vocabulary', path: '/vocabulary' },
  ];

  const handleLogout = async () => {
    try {
      const res = await logout()
      console.log(res)
      navigate('/login')
    }
    catch (error) {
      alert(error.message);
    }
    
  };

  return (
    <aside className="w-64 bg-white border-r border-gray-200 p-6 flex flex-col justify-between h-screen">
      <div>
        <h1 className="text-3xl font-extrabold mb-8 text-gray-900 select-none">
          Language App
        </h1>
        <nav aria-label="Primary" className="flex flex-col space-y-4">
          {links.map(({ name, path }) => {
            const isActive = location.pathname === path;
            return (
              <Link
                key={name}
                to={path}
                aria-current={isActive ? 'page' : undefined}
                className={`
                  block px-4 py-3 rounded-md
                  transition-colors duration-200
                  focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2
                  ${isActive
                    ? 'bg-indigo-100 text-indigo-700 font-semibold'
                    : 'text-gray-700 hover:bg-gray-100 hover:text-gray-900'}
                `}
              >
                {name}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Logout button ở dưới cùng */}
      <button
        onClick={handleLogout}
        className="mt-6 flex items-center px-4 py-3 text-gray-700 hover:bg-gray-100 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors duration-200"
      >
        {/* Icon logout (SVG) */}
        <svg
          className="w-5 h-5 mr-3 text-gray-600"
          fill="none"
          stroke="currentColor"
          strokeWidth={2}
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2h4a2 2 0 012 2v1" />
        </svg>
        Logout
      </button>
    </aside>
  );
}

export default Sidebar;
