import Head from 'next/head';
import Link from 'next/link';
import { Layout } from '@/components';

// Mock data for workout history
const mockSessions = [
    {
        id: '1',
        date: '2026-03-18',
        duration_minutes: 60,
        calories_burned: 450,
        notes: 'Heavy chest day, felt strong on bench press.',
        exercises_completed: 5,
        energy_level: 'High',
    },
    {
        id: '2',
        date: '2026-03-16',
        duration_minutes: 45,
        calories_burned: 320,
        notes: 'Quick HIIT session on the treadmill.',
        exercises_completed: 3,
        energy_level: 'Medium',
    },
    {
        id: '3',
        date: '2026-03-15',
        duration_minutes: 90,
        calories_burned: 600,
        notes: 'Leg day. Squats were tough.',
        exercises_completed: 7,
        energy_level: 'Low',
    }
];

export default function WorkoutsDashboard() {
    // Generate simple chart data
    const maxDuration = Math.max(...mockSessions.map(s => s.duration_minutes));

    return (
        <>
            <Head>
                <title>Workouts - GymBuddy</title>
            </Head>
            <Layout>
                <main className="pt-24 pb-16 px-4 min-h-screen">
                    <div className="max-w-4xl mx-auto space-y-8">
                        
                        {/* Header Section */}
                        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                            <div>
                                <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                                    Your Progress
                                </h1>
                                <p className="text-gray-400">
                                    Track your fitness journey and stay consistent
                                </p>
                            </div>
                            <div className="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-4">
                                <Link href="/workouts/plan" className="px-6 py-3 bg-gray-800 hover:bg-gray-700 border border-gray-600 text-white rounded-xl font-medium transition-all flex items-center justify-center space-x-2">
                                    <span>🧠</span>
                                    <span>AI Plan</span>
                                </Link>
                                <Link href="/workouts/log" className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white rounded-xl font-medium transition-all shadow-lg shadow-purple-900/50 flex items-center justify-center space-x-2">
                                    <span>+</span>
                                    <span>Log Workout</span>
                                </Link>
                            </div>
                        </div>

                        {/* Top Stats Cards */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-2xl p-6">
                                <h3 className="text-gray-400 text-sm font-medium mb-1">Total Sessions</h3>
                                <p className="text-3xl font-bold text-white">{mockSessions.length}</p>
                            </div>
                            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-2xl p-6">
                                <h3 className="text-gray-400 text-sm font-medium mb-1">Total Minutes</h3>
                                <p className="text-3xl font-bold text-white">
                                    {mockSessions.reduce((acc, curr) => acc + curr.duration_minutes, 0)}
                                </p>
                            </div>
                            <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-2xl p-6">
                                <h3 className="text-gray-400 text-sm font-medium mb-1">Calories Burned</h3>
                                <p className="text-3xl font-bold text-white">
                                    {mockSessions.reduce((acc, curr) => acc + (curr.calories_burned || 0), 0)}
                                </p>
                            </div>
                        </div>

                        {/* Trend Chart (CSS only) */}
                        <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-2xl p-6">
                            <h3 className="text-white font-semibold mb-6">Duration Trend (Minutes)</h3>
                            <div className="h-48 flex items-end space-x-4 md:space-x-8">
                                {[...mockSessions].reverse().map((session, idx) => {
                                    const heightPercentage = (session.duration_minutes / maxDuration) * 100;
                                    return (
                                        <div key={idx} className="flex-1 flex flex-col items-center group relative">
                                            {/* Tooltip */}
                                            <div className="absolute -top-10 opacity-0 group-hover:opacity-100 transition-opacity bg-gray-900 text-white text-xs py-1 px-2 rounded pointer-events-none whitespace-nowrap">
                                                {session.duration_minutes} min
                                            </div>
                                            {/* Bar */}
                                            <div 
                                                className="w-full bg-gradient-to-t from-purple-600 to-pink-500 rounded-t-sm transition-all duration-500 ease-out"
                                                style={{ height: `${heightPercentage}%` }}
                                            />
                                            {/* Date */}
                                            <span className="text-[10px] md:text-xs text-gray-500 mt-2 truncate">
                                                {new Date(session.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                                            </span>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>

                        {/* Recent History List */}
                        <div>
                            <h3 className="text-xl font-bold text-white mb-4">Recent Sessions</h3>
                            <div className="space-y-4">
                                {mockSessions.map((session) => (
                                    <div key={session.id} className="bg-gray-800/30 border border-gray-700 rounded-2xl p-5 hover:bg-gray-800/50 transition-colors">
                                        <div className="flex flex-col md:flex-row justify-between gap-4">
                                            <div>
                                                <div className="flex items-center space-x-3 mb-2">
                                                    <span className="text-purple-400 font-semibold text-lg">
                                                        {new Date(session.date).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })}
                                                    </span>
                                                    <span className="px-2 py-1 bg-gray-700 text-xs rounded text-gray-300">
                                                        {session.energy_level} Energy
                                                    </span>
                                                </div>
                                                <p className="text-gray-300 text-sm">{session.notes}</p>
                                            </div>
                                            
                                            <div className="flex space-x-4 md:flex-col md:space-x-0 md:space-y-2 md:text-right">
                                                <div>
                                                    <span className="block text-xs text-gray-500 uppercase tracking-wide">Duration</span>
                                                    <span className="font-semibold text-white">{session.duration_minutes} min</span>
                                                </div>
                                                <div>
                                                    <span className="block text-xs text-gray-500 uppercase tracking-wide">Calories</span>
                                                    <span className="font-semibold text-white">{session.calories_burned} kcal</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                    </div>
                </main>
            </Layout>
        </>
    );
}
