import Link from 'next/link';
import { useState } from 'react';

export default function Navbar() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 bg-gray-900/80 backdrop-blur-md border-b border-gray-700/50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    {/* Logo */}
                    <Link href="/" className="flex items-center space-x-2">
                        <span className="text-2xl">🏋️</span>
                        <span className="text-xl font-bold text-white">
                            Gym<span className="text-purple-400">Buddy</span>
                        </span>
                    </Link>

                    {/* Desktop Navigation */}
                    <div className="hidden md:flex items-center space-x-8">
                        <Link href="/discover" className="text-gray-300 hover:text-white transition-colors">
                            Discover
                        </Link>
                        <Link href="/matches" className="text-gray-300 hover:text-white transition-colors">
                            Matches
                        </Link>
                        <Link href="/profile" className="text-gray-300 hover:text-white transition-colors">
                            Profile
                        </Link>
                    </div>

                    {/* Auth Buttons */}
                    <div className="hidden md:flex items-center space-x-4">
                        <Link
                            href="/login"
                            className="text-gray-300 hover:text-white transition-colors"
                        >
                            Login
                        </Link>
                        <Link
                            href="/signup"
                            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-all duration-200"
                        >
                            Sign Up
                        </Link>
                    </div>

                    {/* Mobile Menu Button */}
                    <button
                        className="md:hidden text-gray-300"
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                    >
                        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            {isMenuOpen ? (
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                            ) : (
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                            )}
                        </svg>
                    </button>
                </div>

                {/* Mobile Menu */}
                {isMenuOpen && (
                    <div className="md:hidden py-4 space-y-4">
                        <Link href="/discover" className="block text-gray-300 hover:text-white">
                            Discover
                        </Link>
                        <Link href="/matches" className="block text-gray-300 hover:text-white">
                            Matches
                        </Link>
                        <Link href="/profile" className="block text-gray-300 hover:text-white">
                            Profile
                        </Link>
                        <div className="pt-4 space-y-2">
                            <Link href="/login" className="block text-gray-300 hover:text-white">
                                Login
                            </Link>
                            <Link
                                href="/signup"
                                className="block px-4 py-2 bg-purple-600 text-white rounded-lg text-center"
                            >
                                Sign Up
                            </Link>
                        </div>
                    </div>
                )}
            </div>
        </nav>
    );
}
