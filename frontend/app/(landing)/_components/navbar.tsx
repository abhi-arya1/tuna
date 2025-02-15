import React from 'react';

interface NavLinkProps {
  href: string;
  label: string;
}

const NavLink: React.FC<NavLinkProps> = ({ href, label }) => (
  <a
    href={href}
    className="text-gray-400 hover:text-white relative py-2 px-1 transition-colors duration-200"
  >
    {label}
  </a>
);

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant: 'primary' | 'outline';
}

const Button: React.FC<ButtonProps> = ({ variant, children, className = '', ...props }) => {
  const baseStyles = "px-5 py-2 font-medium transition-all duration-200";
  const variants = {
    primary: "bg-accent hover:bg-accent-hover text-white",
    outline: "border-2 border-white text-white hover:bg-white hover:text-background"
  };

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

const Logo: React.FC = () => (
  <div className="flex items-center gap-3">
    <div className="w-10 h-10 bg-accent text-white flex items-center justify-center">
      <span className="font-bold text-lg">T</span>
    </div>
    <span className="font-bold text-lg text-white">Tuna</span>
  </div>
);

const Navbar: React.FC = () => {
  return (
    <header className="fixed top-0 left-0 right-0 bg-background z-50">
      <div className="h-20 border-b border-gray-700">
        <nav className="max-w-7xl mx-auto px-8 h-full flex items-center justify-between">
          <Logo />

          <div className="flex items-center gap-8">
            <NavLink href="#docs" label="Docs" />
            <NavLink href="#use-cases" label="Use Cases" />
            <NavLink href="#blog" label="Blog" />

            <div className="flex items-center gap-4">
              <Button variant="primary">
                Sign Up
              </Button>
              <Button variant="outline">
                Log In
              </Button>
            </div>
          </div>
        </nav>
      </div>
    </header>
  );
};

export default Navbar;
