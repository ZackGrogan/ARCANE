import { NextPage } from 'next';
import Head from 'next/head';
import ProfilePictureGenerator from '../components/ProfilePictureGenerator';

const ProfilePicturesPage: NextPage = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>Profile Picture Generator - ARCANE</title>
        <meta name="description" content="Generate character portraits for your D&D campaign" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          Profile Picture Generator
        </h1>
        
        <ProfilePictureGenerator />
      </main>
    </div>
  );
};

export default ProfilePicturesPage;
