import Head from 'next/head';
import Link from 'next/link';
import { useState } from 'react';
import { useRouter } from 'next/router';
import { Layout } from '@/components';

export default function Login() {
    const router = useRouter();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            const res = await fetch('http://localhost:8000/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            const data = await res.json();
            if (!res.ok) {
                throw new Error(data.detail || 'Invalid email or password');
            }

            // Save token
            localStorage.setItem('token', data.access_token);
            
            // Redirect to dashboard or discover
            router.push('/discover');
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
            <Head>
                <title>Login - GymBuddy</title>
                <meta name="description" content="Login to your GymBuddy account" />
            </Head>
            <Layout showNavbar={false}>
                <main className="min-h-screen flex items-center justify-center px-4">
                    <div className="w-full max-w-md">
                        {/* Logo */}
                        <Link href="/" className="flex items-center justify-center space-x-2 mb-8">
                            <span className="text-3xl">🏋️</span>
                            <span className="text-2xl font-bold text-white">
                                Gym<span className="text-purple-400">Buddy</span>
                            </span>
                        </Link>

                        {/* Login Card */}
                        <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-8">
                            <h1 className="text-2xl font-bold text-white mb-2 text-center">Welcome Back</h1>
                            <p className="text-gray-400 text-center mb-8">Sign in to find your workout partners</p>

                            {error && <div className="bg-red-500/10 border border-red-500 text-red-500 p-3 rounded-lg mb-6 text-sm">{error}</div>}

                            <form onSubmit={handleSubmit} className="space-y-5">
                                <div>
                                    <label className="block text-gray-300 text-sm font-medium mb-2">
                                        Email
                                    </label>
                                    <input
                                        type="email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
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
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        placeholder="••••••••"
                                        className="w-full px-4 py-3 bg-gray-900/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
                                        required
                                    />
                                </div>

                                <div className="flex items-center justify-between text-sm">
                                    <label className="flex items-center text-gray-400">
                                        <input type="checkbox" className="mr-2 rounded border-gray-700" />
                                        Remember me
                                    </label>
                                    <Link href="/forgot-password" className="text-purple-400 hover:text-purple-300">
                                        Forgot password?
                                    </Link>
                                </div>

                                <button
                                    type="submit"
                                    disabled={isLoading}
                                    className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold rounded-lg transition-all duration-200 disabled:opacity-50"
                                >
                                    {isLoading ? 'Signing In...' : 'Sign In'}
                                </button>
                            </form>

                            {/* Divider */}
                            <div className="flex items-center my-6">
                                <div className="flex-1 border-t border-gray-700"></div>
                                <span className="px-4 text-gray-500 text-sm">or continue with</span>
                                <div className="flex-1 border-t border-gray-700"></div>
                            </div>

                            {/* Social Login */}
                            <div className="grid grid-cols-2 gap-4">
                                <button className="flex items-center justify-center px-4 py-3 border border-gray-700 rounded-lg text-gray-300 hover:bg-gray-700/50 transition-colors">
                                    <span className="mr-2">🔵</span> Google
                                </button>
                                <button className="flex items-center justify-center px-4 py-3 border border-gray-700 rounded-lg text-gray-300 hover:bg-gray-700/50 transition-colors">
                                    <span className="mr-2">⚫</span> Apple
                                </button>
                            </div>
                        </div>

                        {/* Sign Up Link */}
                        <p className="text-center text-gray-400 mt-6">
                            Don't have an account?{' '}
                            <Link href="/signup" className="text-purple-400 hover:text-purple-300 font-medium">
                                Sign up
                            </Link>
                        </p>
                    </div>
                </main>
            </Layout>
        </>
    );
}