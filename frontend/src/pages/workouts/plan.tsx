import { useState } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { Layout } from '@/components';

// Mock response representing the generated plan from the backend /workouts/plans/generate
const MOCK_PLAN = {
    id: "plan-5491",
    name: "Advanced 5-Day Split",
    description: "Auto-generated 5-day body part split plan for build_muscle",
    plan_type: "5-day body part split",
    target_goal: "build_muscle",
    start_date: "2026-03-20",
    end_date: "2026-04-17",
    status: "active",
    plan_data: {
        days: [
            {
                day: "monday",
                focus: "Chest",
                exercises: [
                    { name: "Bench Press", sets: 5, reps: "5" },
                    { name: "Incline Press", sets: 4, reps: "8" },
                    { name: "Cable Flyes", sets: 4, reps: "12" }
                ]
            },
            {
                day: "tuesday",
                focus: "Back",
                exercises: [
                    { name: "Deadlifts", sets: 5, reps: "3" },
                    { name: "Weighted Pull-ups", sets: 4, reps: "6" },
                    { name: "T-Bar Rows", sets: 4, reps: "8" }
                ]
            },
            {
                day: "wednesday",
                focus: "Shoulders",
                exercises: [
                    { name: "Military Press", sets: 4, reps: "6" },
                    { name: "Arnold Press", sets: 4, reps: "10" },
                    { name: "Rear Delt Flyes", sets: 4, reps: "15" }
                ]
            },
            {
                day: "friday",
                focus: "Legs",
                exercises: [
                    { name: "Squats", sets: 5, reps: "5" },
                    { name: "Front Squats", sets: 4, reps: "8" },
                    { name: "Leg Press", sets: 4, reps: "12" }
                ]
            },
            {
                day: "saturday",
                focus: "Arms",
                exercises: [
                    { name: "Barbell Curls", sets: 4, reps: "8" },
                    { name: "Skull Crushers", sets: 4, reps: "10" },
                    { name: "Hammer Curls", sets: 3, reps: "12" }
                ]
            }
        ]
    }
};

export default function MyPlan() {
    const router = useRouter();
    const [plan, setPlan] = useState<any>(MOCK_PLAN);
    const [isGenerating, setIsGenerating] = useState(false);

    const handleGenerateNew = () => {
        setIsGenerating(true);
        // Simulate an API call to POST /workouts/plans/generate
        setTimeout(() => {
            alert("Slight progression applied to your new 4 week plan!");
            setIsGenerating(false);
        }, 1500);
    };

    return (
        <>
            <Head>
                <title>My Plan - GymBuddy</title>
            </Head>
            <Layout>
                <main className="pt-24 pb-16 px-4 min-h-screen">
                    <div className="max-w-4xl mx-auto space-y-8">
                        
                        {/* Header & Controls */}
                        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-gray-800 pb-6">
                            <div>
                                <div className="flex items-center space-x-3 mb-2">
                                    <button onClick={() => router.back()} className="text-gray-400 hover:text-white transition">
                                        &larr;
                                    </button>
                                    <h1 className="text-3xl font-bold text-white">Your Plan</h1>
                                </div>
                                <p className="text-gray-400">
                                    AI-Generated routine based on your fitness goals
                                </p>
                            </div>
                            <button 
                                onClick={handleGenerateNew}
                                disabled={isGenerating}
                                className="px-6 py-2 bg-gray-800 hover:bg-gray-700 border border-gray-600 text-white rounded-xl transition disabled:opacity-50"
                            >
                                {isGenerating ? 'Generating...' : 'Regenerate Plan'}
                            </button>
                        </div>

                        {/* Plan Summary Banner */}
                        {plan && (
                            <div className="bg-gradient-to-tr from-purple-900/60 to-pink-900/40 backdrop-blur-md border border-purple-500/30 rounded-3xl p-8 relative overflow-hidden">
                                <div className="absolute top-0 right-0 p-8 opacity-10 text-9xl">🦾</div>
                                <div className="relative z-10">
                                    <span className="bg-purple-600/30 text-purple-300 text-xs font-bold px-3 py-1 rounded-full border border-purple-500/30 mb-4 inline-block uppercase tracking-wider">
                                        {plan.status}
                                    </span>
                                    <h2 className="text-3xl font-bold text-white mb-2">{plan.name}</h2>
                                    <p className="text-gray-300 max-w-lg mb-6 leading-relaxed">
                                        {plan.description}
                                    </p>
                                    <div className="flex space-x-6 text-sm text-gray-400">
                                        <div>
                                            <span className="block text-gray-500 uppercase text-xs font-semibold mb-1">Goal</span>
                                            <span className="text-white bg-gray-900/50 px-3 py-1 rounded-lg border border-gray-700">{plan.target_goal.replace('_', ' ')}</span>
                                        </div>
                                        <div>
                                            <span className="block text-gray-500 uppercase text-xs font-semibold mb-1">Duration</span>
                                            <span className="text-white bg-gray-900/50 px-3 py-1 rounded-lg border border-gray-700">4 Weeks</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Weekly Schedule Breakdown */}
                        {plan && (
                            <div className="space-y-6 pt-4">
                                <h3 className="text-xl font-bold text-white flex items-center">
                                    <span className="w-8 h-8 rounded-full bg-gray-800 flex items-center justify-center mr-3 text-sm">📅</span>
                                    Weekly Breakdown
                                </h3>
                                
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {plan.plan_data.days.map((dayObj: any, idx: number) => (
                                        <div key={idx} className="bg-gray-800/40 border border-gray-700 rounded-2xl p-6 hover:bg-gray-800/60 transition group relative overflow-hidden">
                                            {/* Decorative side border */}
                                            <div className="absolute left-0 top-0 bottom-0 w-1 bg-gradient-to-b from-purple-500 to-pink-500 opacity-50 group-hover:opacity-100 transition-opacity"></div>
                                            
                                            <div className="flex justify-between items-center mb-4">
                                                <h4 className="text-lg font-bold text-white capitalize">{dayObj.day}</h4>
                                                <span className="text-xs bg-purple-900/50 text-purple-300 px-2 py-1 rounded uppercase tracking-wider font-semibold">
                                                    {dayObj.focus}
                                                </span>
                                            </div>
                                            
                                            <ul className="space-y-3">
                                                {dayObj.exercises.map((ex: any, eIdx: number) => (
                                                    <li key={eIdx} className="flex justify-between items-center border-b border-gray-700/50 pb-2 last:border-0 last:pb-0">
                                                        <span className="text-gray-300 text-sm font-medium">{ex.name}</span>
                                                        <span className="text-gray-500 text-xs font-mono bg-gray-900 px-2 py-1 rounded">
                                                            {ex.sets} × <span className="text-white">{ex.reps}</span>
                                                        </span>
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {!plan && !isGenerating && (
                            <div className="text-center py-20 bg-gray-800/20 border border-gray-800 rounded-3xl">
                                <div className="text-6xl mb-4">📋</div>
                                <h3 className="text-xl font-bold text-white mb-2">No Plan Found</h3>
                                <p className="text-gray-400 mb-6 max-w-md mx-auto">Please complete your fitness profile so our AI can generate a personalized workout strategy for you.</p>
                                <button className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-xl transition">
                                    Create Profile
                                </button>
                            </div>
                        )}
                        
                    </div>
                </main>
            </Layout>
        </>
    );
}
