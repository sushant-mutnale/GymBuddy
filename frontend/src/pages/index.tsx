import Head from 'next/head';
import Link from 'next/link';
import { Layout, FeatureCard } from '@/components';

const features = [
    {
        icon: '🤖',
        title: 'AI-Powered Matching',
        description: 'Our collaborative filtering algorithm finds partners who complement your workout style and goals.',
    },
    {
        icon: '📅',
        title: 'Schedule Sync',
        description: 'Match with partners who share your preferred workout times and gym locations.',
    },
    {
        icon: '💪',
        title: 'Goal Alignment',
        description: 'Connect with people who have similar fitness goals - from bulking to cardio.',
    },
    {
        icon: '📊',
        title: 'Progress Tracking',
        description: 'Track your workouts together and motivate each other to reach new milestones.',
    },
    {
        icon: '💬',
        title: 'In-App Messaging',
        description: 'Chat with your matched partners to coordinate workouts and build friendships.',
    },
    {
        icon: '⭐',
        title: 'Partner Reviews',
        description: 'See ratings and reviews to find reliable and committed workout partners.',
    },
];

export default function Home() {
    return (
        <>
            <Head>
                <title>GymBuddy - Find Your Perfect Workout Partner</title>
                <meta name="description" content="AI-powered gym partner matching app using collaborative filtering" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <Layout>
                {/* Hero Section */}
                <main className="pt-16">
                    <section className="min-h-screen flex flex-col items-center justify-center px-4 relative overflow-hidden">
                        {/* Background Effects */}
                        <div className="absolute inset-0 overflow-hidden">
                            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl"></div>
                            <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-pink-600/20 rounded-full blur-3xl"></div>
                        </div>

                        <div className="text-center z-10 max-w-4xl mx-auto">
                            <div className="inline-flex items-center px-4 py-2 bg-purple-900/30 border border-purple-500/30 rounded-full text-purple-300 text-sm mb-6">
                                <span className="mr-2">🚀</span> AI-Powered Partner Matching
                            </div>

                            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
                                Find Your Perfect
                                <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400"> Workout Partner</span>
                            </h1>

                            <p className="text-xl md:text-2xl text-gray-300 mb-10 max-w-2xl mx-auto">
                                Connect with like-minded fitness enthusiasts who match your goals, schedule, and workout style.
                            </p>

                            <div className="flex flex-col sm:flex-row gap-4 justify-center">
                                <Link
                                    href="/signup"
                                    className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold rounded-xl transition-all duration-200 transform hover:scale-105 shadow-lg shadow-purple-500/25"
                                >
                                    Get Started Free
                                </Link>
                                <Link
                                    href="/discover"
                                    className="px-8 py-4 border border-gray-600 hover:border-gray-500 text-white font-semibold rounded-xl transition-all duration-200 hover:bg-gray-800/50"
                                >
                                    Explore Partners
                                </Link>
                            </div>

                            {/* Stats */}
                            <div className="flex justify-center gap-12 mt-16">
                                <div className="text-center">
                                    <div className="text-3xl font-bold text-white">10K+</div>
                                    <div className="text-gray-400 text-sm">Active Users</div>
                                </div>
                                <div className="text-center">
                                    <div className="text-3xl font-bold text-white">95%</div>
                                    <div className="text-gray-400 text-sm">Match Rate</div>
                                </div>
                                <div className="text-center">
                                    <div className="text-3xl font-bold text-white">50+</div>
                                    <div className="text-gray-400 text-sm">Gyms</div>
                                </div>
                            </div>
                        </div>
                    </section>

                    {/* Features Section */}
                    <section className="py-24 px-4">
                        <div className="max-w-6xl mx-auto">
                            <div className="text-center mb-16">
                                <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                                    Why Choose GymBuddy?
                                </h2>
                                <p className="text-gray-400 max-w-2xl mx-auto">
                                    Our intelligent matching system ensures you find the perfect workout partner every time.
                                </p>
                            </div>

                            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {features.map((feature, idx) => (
                                    <FeatureCard key={idx} {...feature} />
                                ))}
                            </div>
                        </div>
                    </section>

                    {/* CTA Section */}
                    <section className="py-24 px-4">
                        <div className="max-w-4xl mx-auto text-center bg-gradient-to-r from-purple-900/50 to-pink-900/50 border border-purple-500/20 rounded-3xl p-12">
                            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                                Ready to Find Your Gym Partner?
                            </h2>
                            <p className="text-gray-300 mb-8 max-w-xl mx-auto">
                                Join thousands of fitness enthusiasts who have found their perfect workout partners.
                            </p>
                            <Link
                                href="/signup"
                                className="inline-block px-8 py-4 bg-white text-purple-900 font-semibold rounded-xl hover:bg-gray-100 transition-colors"
                            >
                                Start Matching Today
                            </Link>
                        </div>
                    </section>

                    {/* Footer */}
                    <footer className="py-12 border-t border-gray-800">
                        <div className="max-w-6xl mx-auto px-4 text-center text-gray-500">
                            <div className="flex items-center justify-center space-x-2 mb-4">
                                <span className="text-2xl">🏋️</span>
                                <span className="text-xl font-bold text-white">
                                    Gym<span className="text-purple-400">Buddy</span>
                                </span>
                            </div>
                            <p className="text-sm">
                                Built with ❤️ for fitness enthusiasts • © 2026 GymBuddy
                            </p>
                        </div>
                    </footer>
                </main>
            </Layout>
        </>
    );
}
