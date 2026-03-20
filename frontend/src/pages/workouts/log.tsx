import { useState } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import { Layout } from '@/components';

export default function LogWorkout() {
    const router = useRouter();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [formData, setFormData] = useState({
        date: new Date().toISOString().split('T')[0],
        duration_minutes: 60,
        calories_burned: '',
        exercises_completed: '',
        energy_level: 'Medium',
        notes: ''
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        
        // Mock API call to backend /workouts/sessions
        try {
            await new Promise(resolve => setTimeout(resolve, 800)); // Simulate network request
            router.push('/workouts');
        } catch (error) {
            console.error(error);
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <>
            <Head>
                <title>Log Workout - GymBuddy</title>
            </Head>
            <Layout>
                <main className="pt-24 pb-16 px-4 min-h-screen">
                    <div className="max-w-2xl mx-auto">
                        <div className="mb-8">
                            <button onClick={() => router.back()} className="text-gray-400 hover:text-white transition flex items-center space-x-2 mb-4">
                                <span>&larr;</span>
                                <span>Back to Dashboard</span>
                            </button>
                            <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                                Log Session
                            </h1>
                            <p className="text-gray-400">
                                Record your workout to track your progress over time.
                            </p>
                        </div>

                        <form onSubmit={handleSubmit} className="bg-gray-800/50 backdrop-blur-md border border-gray-700 rounded-3xl p-6 md:p-8 space-y-6 shadow-2xl">
                            
                            {/* Date & Duration */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-gray-300">Date</label>
                                    <input 
                                        type="date"
                                        name="date"
                                        required
                                        value={formData.date}
                                        onChange={handleChange}
                                        className="w-full bg-gray-900 border border-gray-700 text-white rounded-xl px-4 py-3 focus:outline-none focus:border-purple-500 transition"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-gray-300">Duration (Minutes)</label>
                                    <input 
                                        type="number"
                                        name="duration_minutes"
                                        required
                                        min="1"
                                        value={formData.duration_minutes}
                                        onChange={handleChange}
                                        className="w-full bg-gray-900 border border-gray-700 text-white rounded-xl px-4 py-3 focus:outline-none focus:border-purple-500 transition"
                                    />
                                </div>
                            </div>

                            {/* Details row */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-gray-300">Calories Burned (Est.)</label>
                                    <input 
                                        type="number"
                                        name="calories_burned"
                                        placeholder="e.g. 400"
                                        value={formData.calories_burned}
                                        onChange={handleChange}
                                        className="w-full bg-gray-900 border border-gray-700 text-white rounded-xl px-4 py-3 focus:outline-none focus:border-purple-500 transition"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-gray-300">Exercises Completed</label>
                                    <input 
                                        type="number"
                                        name="exercises_completed"
                                        placeholder="e.g. 5"
                                        value={formData.exercises_completed}
                                        onChange={handleChange}
                                        className="w-full bg-gray-900 border border-gray-700 text-white rounded-xl px-4 py-3 focus:outline-none focus:border-purple-500 transition"
                                    />
                                </div>
                            </div>

                            {/* Energy Level */}
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-300">Energy Level</label>
                                <select 
                                    name="energy_level"
                                    value={formData.energy_level}
                                    onChange={handleChange}
                                    className="w-full bg-gray-900 border border-gray-700 text-white rounded-xl px-4 py-3 focus:outline-none focus:border-purple-500 transition appearance-none"
                                >
                                    <option value="Very Low">Very Low</option>
                                    <option value="Low">Low</option>
                                    <option value="Medium">Medium</option>
                                    <option value="High">High</option>
                                    <option value="Beast Mode">Beast Mode 🦍</option>
                                </select>
                            </div>

                            {/* Notes */}
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-300">Workout Notes</label>
                                <textarea 
                                    name="notes"
                                    rows={4}
                                    placeholder="How did you feel? Hit any PRs? Form checks?"
                                    value={formData.notes}
                                    onChange={handleChange}
                                    className="w-full bg-gray-900 border border-gray-700 text-white rounded-xl px-4 py-3 focus:outline-none focus:border-purple-500 transition resize-none"
                                />
                            </div>

                            {/* Submit */}
                            <button 
                                type="submit" 
                                disabled={isSubmitting}
                                className="w-full py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white rounded-xl font-bold text-lg transition-all shadow-lg shadow-purple-900/50 disabled:opacity-70 disabled:cursor-not-allowed"
                            >
                                {isSubmitting ? 'Saving Session...' : 'Save Workout'}
                            </button>
                        </form>

                    </div>
                </main>
            </Layout>
        </>
    );
}
