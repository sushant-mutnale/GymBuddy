import Head from 'next/head';
import { Layout } from '@/components';

// Mock matches data
const mockMatches = [
    {
        name: 'Alex Chen',
        matchScore: 95,
        workoutTypes: ['Strength Training', 'HIIT'],
        lastMessage: 'Ready for tomorrow morning?',
        lastActive: '2 min ago',
        unread: 2,
    },
    {
        name: 'Sarah Miller',
        matchScore: 88,
        workoutTypes: ['CrossFit', 'Cardio'],
        lastMessage: 'Great workout today! 💪',
        lastActive: '1 hour ago',
        unread: 0,
    },
    {
        name: 'Marcus Johnson',
        matchScore: 82,
        workoutTypes: ['Powerlifting'],
        lastMessage: 'Let me know when you want to hit legs',
        lastActive: 'Yesterday',
        unread: 0,
    },
];

const pendingRequests = [
    {
        name: 'Emily Rodriguez',
        matchScore: 79,
        workoutTypes: ['Yoga', 'Pilates'],
    },
    {
        name: 'Jake Thompson',
        matchScore: 75,
        workoutTypes: ['Boxing', 'Functional'],
    },
];

export default function Matches() {
    return (
        <>
            <Head>
                <title>Matches - GymBuddy</title>
                <meta name="description" content="Your workout partner matches" />
            </Head>
            <Layout>
                <main className="pt-24 pb-16 px-4">
                    <div className="max-w-4xl mx-auto">
                        {/* Header */}
                        <div className="mb-8">
                            <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                                Your Matches
                            </h1>
                            <p className="text-gray-400">
                                Connect with your workout partners
                            </p>
                        </div>

                        {/* Pending Requests */}
                        {pendingRequests.length > 0 && (
                            <div className="mb-8">
                                <h2 className="text-lg font-semibold text-white mb-4 flex items-center">
                                    <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                                    Pending Requests ({pendingRequests.length})
                                </h2>
                                <div className="space-y-3">
                                    {pendingRequests.map((request, idx) => (
                                        <div
                                            key={idx}
                                            className="bg-gray-800/50 backdrop-blur-sm border border-purple-500/30 rounded-xl p-4 flex items-center justify-between"
                                        >
                                            <div className="flex items-center space-x-4">
                                                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-xl">
                                                    💪
                                                </div>
                                                <div>
                                                    <h3 className="font-semibold text-white">{request.name}</h3>
                                                    <div className="flex items-center space-x-2 text-sm">
                                                        <span className="text-purple-400">{request.matchScore}% match</span>
                                                        <span className="text-gray-600">•</span>
                                                        <span className="text-gray-400">{request.workoutTypes.join(', ')}</span>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="flex space-x-2">
                                                <button className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-sm font-medium transition-colors">
                                                    Accept
                                                </button>
                                                <button className="px-4 py-2 border border-gray-600 hover:border-gray-500 text-gray-300 rounded-lg text-sm transition-colors">
                                                    Decline
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Active Matches */}
                        <div>
                            <h2 className="text-lg font-semibold text-white mb-4">
                                Active Partners ({mockMatches.length})
                            </h2>
                            <div className="space-y-3">
                                {mockMatches.map((match, idx) => (
                                    <div
                                        key={idx}
                                        className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-4 hover:border-gray-600 transition-colors cursor-pointer"
                                    >
                                        <div className="flex items-center space-x-4">
                                            <div className="relative">
                                                <div className="w-14 h-14 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-2xl">
                                                    💪
                                                </div>
                                                {match.unread > 0 && (
                                                    <div className="absolute -top-1 -right-1 w-5 h-5 bg-purple-500 rounded-full flex items-center justify-center text-xs text-white font-bold">
                                                        {match.unread}
                                                    </div>
                                                )}
                                            </div>
                                            <div className="flex-1 min-w-0">
                                                <div className="flex items-center justify-between mb-1">
                                                    <h3 className="font-semibold text-white">{match.name}</h3>
                                                    <span className="text-gray-500 text-xs">{match.lastActive}</span>
                                                </div>
                                                <p className="text-gray-400 text-sm truncate">{match.lastMessage}</p>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Empty State */}
                        {mockMatches.length === 0 && (
                            <div className="text-center py-16">
                                <div className="text-6xl mb-4">🤝</div>
                                <h3 className="text-xl font-semibold text-white mb-2">No matches yet</h3>
                                <p className="text-gray-400 mb-6">Start discovering partners to make your first connection</p>
                                <a
                                    href="/discover"
                                    className="inline-block px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors"
                                >
                                    Discover Partners
                                </a>
                            </div>
                        )}
                    </div>
                </main>
            </Layout>
        </>
    );
}
