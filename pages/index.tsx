import { NextPage } from 'next';
import Link from 'next/link';
import Head from 'next/head';

const Home: NextPage = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>ARCANE - AI-Driven RPG Campaign Assistant & Narrative Engine</title>
        <meta name="description" content="Your ultimate D&D campaign management tool" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          Welcome to ARCANE
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* NPC Management */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">NPC Management</h2>
            <p className="text-gray-600 mb-4">Create and manage NPCs for your campaign.</p>
            <Link href="/npcs/create" className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors">
              Create NPC
            </Link>
          </div>

          {/* Random Encounters */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">Random Encounters</h2>
            <p className="text-gray-600 mb-4">Generate dynamic and balanced encounters for your party.</p>
            <Link href="/encounters" className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors">
              Generate Encounter
            </Link>
          </div>

          {/* Profile Pictures */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">Profile Pictures</h2>
            <p className="text-gray-600 mb-4">Generate and manage character portraits.</p>
            <Link href="/profile-pictures" className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors">
              Generate Portrait
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;
