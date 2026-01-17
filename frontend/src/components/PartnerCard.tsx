interface PartnerCardProps {
    name: string;
    age: number;
    location: string;
    workoutTypes: string[];
    schedule: string;
    matchScore: number;
    imageUrl?: string;
}

export default function PartnerCard({
    name,
    age,
    location,
    workoutTypes,
    schedule,
    matchScore,
    imageUrl,
}: PartnerCardProps) {
    return (
        <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-6 hover:border-purple-500/50 transition-all duration-300 hover:shadow-lg hover:shadow-purple-500/10">
            {/* Profile Header */}
            <div className="flex items-start space-x-4 mb-4">
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-2xl">
                    {imageUrl ? (
                        <img src={imageUrl} alt={name} className="w-full h-full rounded-full object-cover" />
                    ) : (
                        <span>💪</span>
                    )}
                </div>
                <div className="flex-1">
                    <h3 className="text-lg font-semibold text-white">{name}</h3>
                    <p className="text-gray-400 text-sm">{age} years old • {location}</p>
                </div>
                <div className="text-right">
                    <div className="text-2xl font-bold text-purple-400">{matchScore}%</div>
                    <p className="text-xs text-gray-500">Match</p>
                </div>
            </div>

            {/* Workout Types */}
            <div className="mb-4">
                <p className="text-gray-500 text-xs mb-2 uppercase tracking-wider">Workouts</p>
                <div className="flex flex-wrap gap-2">
                    {workoutTypes.map((type, idx) => (
                        <span
                            key={idx}
                            className="px-3 py-1 bg-purple-900/30 text-purple-300 rounded-full text-xs"
                        >
                            {type}
                        </span>
                    ))}
                </div>
            </div>

            {/* Schedule */}
            <div className="mb-5">
                <p className="text-gray-500 text-xs mb-1 uppercase tracking-wider">Preferred Time</p>
                <p className="text-gray-300 text-sm">{schedule}</p>
            </div>

            {/* Actions */}
            <div className="flex space-x-3">
                <button className="flex-1 py-2.5 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-colors">
                    Connect
                </button>
                <button className="px-4 py-2.5 border border-gray-600 hover:border-gray-500 text-gray-300 rounded-lg transition-colors">
                    View
                </button>
            </div>
        </div>
    );
}
