// src/components/Sidebar.jsx
import { Link, useLocation } from 'react-router-dom';

function Sidebar() {
  const location = useLocation();

  const links = [
    { name: 'Grammar Check', path: '/' },
    { name: 'Analyze Level', path: '/analyze' },
    { name: 'Writing Feedback', path: '/feedback' },
    { name: 'Vocabulary', path: '/vocabulary' },
  ];

  return (
    <aside className="w-64 bg-white border-r border-gray-200 p-6 flex flex-col">
      <h1 className="text-3xl font-extrabold mb-8 text-gray-900 select-none">
        Language App
      </h1>
      <nav aria-label="Primary" className="flex flex-col space-y-4"> {/* Tăng khoảng cách giữa các Link */}
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
    </aside>
  );
}

export default Sidebar;