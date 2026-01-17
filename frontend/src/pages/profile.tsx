import Head from 'next/head';
import { useState } from 'react';
import { Layout } from '@/components';

// Mock user data
const mockUser = {
    name: 'John Smith',
    email: 'john@example.com',
    age: 28,
    location: 'Downtown Gym',
    bio: 'Fitness enthusiast looking for motivated workout partners. Love strength training and HIIT. Let\'s crush it together! 💪',
    workoutTypes: ['Strength Training', 'HIIT', 'Cardio'],
    schedule: 'Mornings (6-8 AM)',
    goals: ['Build Muscle', 'Increase Strength', 'Stay Consistent'],
    stats: {
        workoutsCompleted: 127,
        partnersMatched: 8,
        activeStreak: 14,
    },
};

export default function Profile() {
    const [isEditing, setIsEditing] = useState(false);

    return (
        <>
            <Head>
                <title>Profile - GymBuddy</title>
                <meta name="description" content="Your GymBuddy profile" />
            </Head>
            <Layout>
                <main className="pt-24 pb-16 px-4">
                    <div className="max-w-4xl mx-auto">
                        {/* Profile Header */}
                        <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-8 mb-6">
                            <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
                                {/* Avatar */}
                                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-4xl">
                                    💪
                                </div>

                                {/* Info */}
                                <div className="flex-1">
                                    <div className="flex flex-col md:flex-row md:items-center gap-4 mb-4">
                                        <h1 className="text-2xl font-bold text-white">{mockUser.name}</h1>
                                        <span className="inline-flex items-center px-3 py-1 bg-green-900/30 text-green-400 rounded-full text-sm">
                                            ✓ Verified
                                        </span>
                                    </div>
                                    <p className="text-gray-400 mb-2">📍 {mockUser.location}</p>
                                    <p className="text-gray-300 max-w-xl">{mockUser.bio}</p>
                                </div>

                                {/* Edit Button */}
                                <button
                                    onClick={() => setIsEditing(!isEditing)}
                                    className="px-6 py-2.5 border border-gray-600 hover:border-gray-500 text-gray-300 rounded-lg transition-colors"
                                >
                                    {isEditing ? 'Save Changes' : 'Edit Profile'}
                                </button>
                            </div>
                        </div>

                        {/* Stats Cards */}
                        <div className="grid grid-cols-3 gap-4 mb-6">
                            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6 text-center">
                                <div className="text-3xl font-bold text-purple-400 mb-1">{mockUser.stats.workoutsCompleted}</div>
                                <div className="text-gray-400 text-sm">Workouts</div>
                            </div>
                            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6 text-center">
                                <div className="text-3xl font-bold text-pink-400 mb-1">{mockUser.stats.partnersMatched}</div>
                                <div className="text-gray-400 text-sm">Partners</div>
                            </div>
                            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6 text-center">
                                <div className="text-3xl font-bold text-orange-400 mb-1">{mockUser.stats.activeStreak}🔥</div>
                                <div className="text-gray-400 text-sm">Day Streak</div>
                            </div>
                        </div>

                        <div className="grid md:grid-cols-2 gap-6">
                            {/* Workout Preferences */}
                            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6">
                                <h2 className="text-lg font-semibold text-white mb-4">Workout Preferences</h2>

                                <div className="mb-4">
                                    <p className="text-gray-500 text-xs uppercase tracking-wider mb-2">Workout Types</p>
                                    <div className="flex flex-wrap gap-2">
                                        {mockUser.workoutTypes.map((type, idx) => (
                                            <span
                                                key={idx}
                                                className="px-3 py-1 bg-purple-900/30 text-purple-300 rounded-full text-sm"
                                            >
                                                {type}
                                            </span>
                                        ))}
                                    </div>
                                </div>

                                <div>
                                    <p className="text-gray-500 text-xs uppercase tracking-wider mb-2">Preferred Schedule</p>
                                    <p className="text-gray-300">{mockUser.schedule}</p>
                                </div>
                            </div>

                            {/* Fitness Goals */}
                            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6">
                                <h2 className="text-lg font-semibold text-white mb-4">Fitness Goals</h2>

                                <div className="space-y-3">
                                    {mockUser.goals.map((goal, idx) => (
                                        <div key={idx} className="flex items-center space-x-3">
                                            <div className="w-8 h-8 bg-gradient-to-br from-purple-600/20 to-pink-600/20 rounded-lg flex items-center justify-center text-sm">
                                                🎯
                                            </div>
                                            <span className="text-gray-300">{goal}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>

                        {/* Recent Activity */}
                        <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-xl p-6 mt-6">
                            <h2 className="text-lg font-semibold text-white mb-4">Recent Activity</h2>

                            <div className="space-y-4">
                                <div className="flex items-center space-x-4 p-3 bg-gray-900/30 rounded-lg">
                                    <div className="w-10 h-10 bg-green-900/30 rounded-full flex items-center justify-center text-lg">✅</div>
                                    <div className="flex-1">
                                        <p className="text-white">Completed workout with Alex Chen</p>
                                        <p className="text-gray-500 text-sm">Strength Training • 2 hours ago</p>
                                    </div>
                                </div>
                                <div className="flex items-center space-x-4 p-3 bg-gray-900/30 rounded-lg">
                                    <div className="w-10 h-10 bg-purple-900/30 rounded-full flex items-center justify-center text-lg">🤝</div>
                                    <div className="flex-1">
                                        <p className="text-white">Matched with Sarah Miller</p>
                                        <p className="text-gray-500 text-sm">88% match score • Yesterday</p>
                                    </div>
                                </div>
                                <div className="flex items-center space-x-4 p-3 bg-gray-900/30 rounded-lg">
                                    <div className="w-10 h-10 bg-orange-900/30 rounded-full flex items-center justify-center text-lg">🔥</div>
                                    <div className="flex-1">
                                        <p className="text-white">Achieved 14-day workout streak!</p>
                                        <p className="text-gray-500 text-sm">Milestone • 3 days ago</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </main>
            </Layout>
        </>
    );
}
