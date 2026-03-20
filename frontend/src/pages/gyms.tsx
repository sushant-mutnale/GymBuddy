import { useState } from 'react';
import Head from 'next/head';
import { Layout } from '@/components';

// Mock Gym Data
const mockGyms = [
    {
        id: 'gym-1',
        name: 'Iron Forge Fitness',
        address: '123 Muscle Ave, Downtown',
        city: 'New York',
        distance_km: 1.2,
        member_count: 45,
        is_active: true
    },
    {
        id: 'gym-2',
        name: 'Planet Workout',
        address: '456 Cardio Blvd',
        city: 'New York',
        distance_km: 2.5,
        member_count: 120,
        is_active: true
    },
    {
        id: 'gym-3',
        name: 'CrossFit Elite',
        address: '789 Strength St',
        city: 'New York',
        distance_km: 3.8,
        member_count: 22,
        is_active: true
    }
];

export default function Gyms() {
    const [searchQuery, setSearchQuery] = useState("");
    const [preferredGymId, setPreferredGymId] = useState<string | null>('gym-1');
    const [isCheckingIn, setIsCheckingIn] = useState(false);

    const filteredGyms = mockGyms.filter(gym => 
        gym.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
        gym.address.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const handleCheckIn = async (gymId: string) => {
        setIsCheckingIn(true);
        // Simulate API call to POST /gyms/{gym_id}/check-in
        setTimeout(() => {
            setPreferredGymId(gymId);
            setIsCheckingIn(false);
            alert("Checked into Gym successfully!");
        }, 600);
    };

    return (
        <>
            <Head>
                <title>Find Gyms - GymBuddy</title>
            </Head>
            <Layout>
                <main className="pt-24 pb-16 px-4 min-h-screen">
                    <div className="max-w-4xl mx-auto space-y-8">
                        
                        {/* Header */}
                        <div>
                            <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                                Gym Locator
                            </h1>
                            <p className="text-gray-400">
                                Find gyms near you, check in, and connect with locals.
                            </p>
                        </div>

                        {/* Search Bar */}
                        <div className="relative">
                            <input 
                                type="text" 
                                placeholder="Search by name, city, or address..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="w-full bg-gray-800 border border-gray-700 text-white rounded-2xl px-6 py-4 focus:outline-none focus:border-purple-500 shadow-inner text-lg pl-14"
                            />
                            <span className="absolute left-5 top-1/2 transform -translate-y-1/2 text-2xl">
                                🔍
                            </span>
                        </div>

                        {/* Gym List */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {filteredGyms.map(gym => {
                                const isPreferred = gym.id === preferredGymId;
                                
                                return (
                                    <div 
                                        key={gym.id} 
                                        className={`bg-gray-800/50 backdrop-blur-sm border rounded-2xl p-6 transition-all duration-300 ${isPreferred ? 'border-purple-500 shadow-lg shadow-purple-900/40' : 'border-gray-700 hover:border-gray-500'}`}
                                    >
                                        <div className="flex justify-between items-start mb-4">
                                            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-xl shadow-md">
                                                🏢
                                            </div>
                                            {isPreferred && (
                                                <span className="bg-purple-600/20 text-purple-400 text-xs font-bold px-3 py-1 rounded-full border border-purple-500/30">
                                                    Your Gym
                                                </span>
                                            )}
                                        </div>
                                        
                                        <h3 className="text-xl font-bold text-white mb-1">{gym.name}</h3>
                                        <p className="text-gray-400 text-sm mb-4 line-clamp-2">{gym.address}, {gym.city}</p>
                                        
                                        <div className="flex items-center space-x-4 mb-6 text-sm">
                                            <div className="flex items-center text-gray-300">
                                                <span className="mr-1">📍</span> {gym.distance_km} km
                                            </div>
                                            <div className="flex items-center text-gray-300">
                                                <span className="mr-1">👥</span> {gym.member_count} active
                                            </div>
                                        </div>
                                        
                                        <button 
                                            onClick={() => handleCheckIn(gym.id)}
                                            disabled={isPreferred || isCheckingIn}
                                            className={`w-full py-3 rounded-xl font-medium transition ${
                                                isPreferred 
                                                ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
                                                : 'bg-transparent border border-purple-500 text-purple-400 hover:bg-purple-600 hover:text-white pointer'
                                            }`}
                                        >
                                            {isPreferred ? 'Current Gym' : 'Check In'}
                                        </button>
                                    </div>
                                );
                            })}
                        </div>
                        
                        {filteredGyms.length === 0 && (
                            <div className="text-center py-20">
                                <span className="text-6xl block mb-4">🏜️</span>
                                <h3 className="text-2xl font-bold text-white mb-2">No Gyms Found</h3>
                                <p className="text-gray-400">Try adjusting your search criteria or register a new gym.</p>
                            </div>
                        )}

                    </div>
                </main>
            </Layout>
        </>
    );
}
