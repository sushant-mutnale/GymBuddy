import Head from 'next/head';
import Link from 'next/link';
import { useState } from 'react';
import { Layout } from '@/components';

export default function Signup() {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        // TODO: Implement signup logic
        console.log('Signup:', formData);
    };

    return (
        <>
            <Head>
                <title>Sign Up - GymBuddy</title>
                <meta name="description" content="Create your GymBuddy account" />
            </Head>
            <Layout showNavbar={false}>
                <main className="min-h-screen flex items-center justify-center px-4 py-12">
                    <div className="w-full max-w-md">
                        {/* Logo */}
                        <Link href="/" className="flex items-center justify-center space-x-2 mb-8">
                            <span className="text-3xl">🏋️</span>
                            <span className="text-2xl font-bold text-white">
                                Gym<span className="text-purple-400">Buddy</span>
                            </span>
                        </Link>

                        {/* Signup Card */}
                        <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-8">
                            <h1 className="text-2xl font-bold text-white mb-2 text-center">Create Account</h1>
                            <p className="text-gray-400 text-center mb-8">Start finding your perfect workout partners</p>

                            <form onSubmit={handleSubmit} className="space-y-5">
                                <div>
                                    <label className="block text-gray-300 text-sm font-medium mb-2">
                                        Full Name
                                    </label>
                                    <input
                                        type="text"
                                        name="name"
                                        value={formData.name}
                                        onChange={handleChange}
                                        placeholder="John Doe"
                                        className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
                                        required
                                    />
                                </div>

                                <div>
                                    <label className="block text-gray-300 text-sm font-medium mb-2">
                                        Email
                                    </label>
                                    <input
                                        type="email"
                                        name="email"
                                        value={formData.email}
                                        onChange={handleChange}
                                        placeholder="you@example.com"
                                        className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
                                        required
                                    />
                                </div>

                                <div>
                                    <label className="block text-gray-300 text-sm font-medium mb-2">
                                        Password
                                    </label>
                                    <input
                                        type="password"
                                        name="password"
                                        value={formData.password}
                                        onChange={handleChange}
                                        placeholder="••••••••"
                                        className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
                                        required
                                    />
                                </div>

                                <div>
                                    <label className="block text-gray-300 text-sm font-medium mb-2">
                                        Confirm Password
                                    </label>
                                    <input
                                        type="password"
                                        name="confirmPassword"
                                        value={formData.confirmPassword}
                                        onChange={handleChange}
                                        placeholder="••••••••"
                                        className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
                                        required
                                    />
                                </div>

                                <div className="text-sm text-gray-400">
                                    <label className="flex items-start">
                                        <input type="checkbox" className="mr-2 mt-1 rounded border-gray-700" required />
                                        <span>
                                            I agree to the{' '}
                                            <Link href="/terms" className="text-purple-400 hover:text-purple-300">
                                                Terms of Service
                                            </Link>{' '}
                                            and{' '}
                                            <Link href="/privacy" className="text-purple-400 hover:text-purple-300">
                                                Privacy Policy
                                            </Link>
                                        </span>
                                    </label>
                                </div>

                                <button
                                    type="submit"
                                    className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold rounded-lg transition-all duration-200"
                                >
                                    Create Account
                                </button>
                            </form>

                            {/* Divider */}
                            <div className="flex items-center my-6">
                                <div className="flex-1 border-t border-gray-700"></div>
                                <span className="px-4 text-gray-500 text-sm">or sign up with</span>
                                <div className="flex-1 border-t border-gray-700"></div>
                            </div>

                            {/* Social Signup */}
                            <div className="grid grid-cols-2 gap-4">
                                <button className="flex items-center justify-center px-4 py-3 border border-gray-700 rounded-lg text-gray-300 hover:bg-gray-700/50 transition-colors">
                                    <span className="mr-2">🔵</span> Google
                                </button>
                                <button className="flex items-center justify-center px-4 py-3 border border-gray-700 rounded-lg text-gray-300 hover:bg-gray-700/50 transition-colors">
                                    <span className="mr-2">⚫</span> Apple
                                </button>
                            </div>
                        </div>

                        {/* Login Link */}
                        <p className="text-center text-gray-400 mt-6">
                            Already have an account?{' '}
                            <Link href="/login" className="text-purple-400 hover:text-purple-300 font-medium">
                                Sign in
                            </Link>
                        </p>
                    </div>
                </main>
            </Layout>
        </>
    );
}
