import Head from 'next/head';
import { useState } from 'react';
import { Layout, PartnerCard } from '@/components';

// Mock data for demo
const mockPartners = [
    {
        name: 'Alex Chen',
        age: 28,
        location: 'Downtown Gym',
        workoutTypes: ['Strength Training', 'HIIT'],
        schedule: 'Mornings (6-8 AM)',
        matchScore: 95,
    },
    {
        name: 'Sarah Miller',
        age: 25,
        location: 'FitLife Center',
        workoutTypes: ['CrossFit', 'Cardio'],
        schedule: 'Evenings (6-8 PM)',
        matchScore: 88,
    },
    {
        name: 'Marcus Johnson',
        age: 32,
        location: 'PowerHouse Gym',
        workoutTypes: ['Powerlifting', 'Bodybuilding'],
        schedule: 'Afternoons (2-5 PM)',
        matchScore: 82,
    },
    {
        name: 'Emily Rodriguez',
        age: 27,
        location: 'Downtown Gym',
        workoutTypes: ['Yoga', 'Pilates', 'Cardio'],
        schedule: 'Mornings (7-9 AM)',
        matchScore: 79,
    },
    {
        name: 'Jake Thompson',
        age: 30,
        location: 'FitLife Center',
        workoutTypes: ['Functional Training', 'Boxing'],
        schedule: 'Evenings (7-9 PM)',
        matchScore: 75,
    },
    {
        name: 'Priya Patel',
        age: 24,
        location: 'PowerHouse Gym',
        workoutTypes: ['Strength Training', 'Swimming'],
        schedule: 'Mornings (5-7 AM)',
        matchScore: 71,
    },
];

const workoutFilters = ['All', 'Strength Training', 'CrossFit', 'Cardio', 'HIIT', 'Yoga', 'Powerlifting'];

export default function Discover() {
    const [selectedFilter, setSelectedFilter] = useState('All');
    const [searchQuery, setSearchQuery] = useState('');

    const filteredPartners = mockPartners.filter(partner => {
        const matchesFilter = selectedFilter === 'All' || partner.workoutTypes.includes(selectedFilter);
        const matchesSearch = partner.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            partner.location.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesFilter && matchesSearch;
    });

    return (
        <>
            <Head>
                <title>Discover Partners - GymBuddy</title>
                <meta name="description" content="Find your perfect workout partner" />
            </Head>
            <Layout>
                <main className="pt-24 pb-16 px-4">
                    <div className="max-w-6xl mx-auto">
                        {/* Header */}
                        <div className="mb-8">
                            <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                                Discover Partners
                            </h1>
                            <p className="text-gray-400">
                                Find workout partners matched to your fitness style
                            </p>
                        </div>

                        {/* Search & Filters */}
                        <div className="mb-8 space-y-4">
                            {/* Search Bar */}
                            <div className="relative">
                                <input
                                    type="text"
                                    placeholder="Search by name or gym..."
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    className="w-full px-5 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
                                />
                                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500">
                                    🔍
                                </span>
                            </div>

                            {/* Filter Pills */}
                            <div className="flex flex-wrap gap-2">
                                {workoutFilters.map((filter) => (
                                    <button
                                        key={filter}
                                        onClick={() => setSelectedFilter(filter)}
                                        className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${selectedFilter === filter
                                                ? 'bg-purple-600 text-white'
                                                : 'bg-gray-800/50 text-gray-400 hover:bg-gray-700/50 hover:text-white'
                                            }`}
                                    >
                                        {filter}
                                    </button>
                                ))}
                            </div>
                        </div>

                        {/* Results Count */}
                        <p className="text-gray-500 text-sm mb-6">
                            Showing {filteredPartners.length} potential partners
                        </p>

                        {/* Partner Grid */}
                        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {filteredPartners.map((partner, idx) => (
                                <PartnerCard key={idx} {...partner} />
                            ))}
                        </div>

                        {/* Empty State */}
                        {filteredPartners.length === 0 && (
                            <div className="text-center py-16">
                                <div className="text-6xl mb-4">🔍</div>
                                <h3 className="text-xl font-semibold text-white mb-2">No partners found</h3>
                                <p className="text-gray-400">Try adjusting your search or filters</p>
                            </div>
                        )}
                    </div>
                </main>
            </Layout>
        </>
    );
}
