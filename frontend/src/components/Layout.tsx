import Navbar from './Navbar';

interface LayoutProps {
    children: React.ReactNode;
    showNavbar?: boolean;
}

export default function Layout({ children, showNavbar = true }: LayoutProps) {
    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900/20 to-gray-900">
            {showNavbar && <Navbar />}
            {children}
        </div>
    );
}
