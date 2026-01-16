import Head from 'next/head'

export default function Home() {
    return (
        <>
            <Head>
                <title>GymBuddy - Find Your Perfect Workout Partner</title>
                <meta name="description" content="AI-powered gym partner matching app using collaborative filtering" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <link rel="icon" href="/favicon.ico" />
            </Head>
            <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
                <div className="text-center px-4">
                    <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
                        🏋️ Gym<span className="text-purple-400">Buddy</span>
                    </h1>
                    <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-2xl">
                        Find your perfect workout partner with AI-powered matching
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <button className="px-8 py-3 bg-purple-600 hover:bg-purple-700 text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105">
                            Get Started
                        </button>
                        <button className="px-8 py-3 border border-purple-400 text-purple-400 hover:bg-purple-400 hover:text-white font-semibold rounded-lg transition-all duration-200">
                            Learn More
                        </button>
                    </div>
                </div>
                <footer className="absolute bottom-8 text-gray-500 text-sm">
                    Built with ❤️ for fitness enthusiasts
                </footer>
            </main>
        </>
    )
}
