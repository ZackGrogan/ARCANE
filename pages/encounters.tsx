import { NextPage } from 'next';
import Head from 'next/head';
import EncounterGenerator from '../components/EncounterGenerator';

const EncountersPage: NextPage = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>Random Encounters Generator - ARCANE</title>
        <meta name="description" content="Generate balanced and engaging D&D encounters" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          Random Encounters Generator
        </h1>
        
        <EncounterGenerator />
      </main>
    </div>
  );
};

export default EncountersPage;
