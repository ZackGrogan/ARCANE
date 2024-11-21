import { GetServerSideProps } from 'next';
import { useRouter } from 'next/router';
import { useState } from 'react';
import dynamic from 'next/dynamic';
import Head from 'next/head';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { toast } from '@/components/ui/use-toast';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { NPC } from '@/types/npc';
import { dbConnect } from '@/lib/dbConnect';
import { NPC as NPCModel } from '@/models/npc';

const ReactQuill = dynamic(() => import('react-quill'), { ssr: false });
import 'react-quill/dist/quill.snow.css';

interface NPCProfileProps {
  initialNPC: NPC | null;
  error?: string;
}

const NPCProfile = ({ initialNPC, error: initialError }: NPCProfileProps) => {
  const router = useRouter();
  const { id } = router.query;
  const [npc, setNpc] = useState<NPC | null>(initialNPC);
  const [editedNpc, setEditedNpc] = useState<NPC | null>(initialNPC);
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(initialError || '');

  // Optimistic update handler
  const handleOptimisticUpdate = async (field: keyof NPC, value: any) => {
    if (!editedNpc) return;
    
    const previousValue = editedNpc[field];
    setEditedNpc(prev => prev ? { ...prev, [field]: value } : null);

    try {
      const response = await fetch(`/api/npcs/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ [field]: value }),
      });

      if (!response.ok) throw new Error('Failed to update field');
      
      const updatedNPC = await response.json();
      setNpc(updatedNPC);
      setEditedNpc(updatedNPC);
      toast({
        title: 'Success',
        description: 'Field updated successfully',
      });
    } catch (err) {
      // Revert on error
      setEditedNpc(prev => prev ? { ...prev, [field]: previousValue } : null);
      toast({
        title: 'Error',
        description: 'Failed to update field. Changes reverted.',
        variant: 'destructive',
      });
    }
  };

  const handleSave = async () => {
    if (!editedNpc) return;
    setLoading(true);
    
    try {
      const response = await fetch(`/api/npcs/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editedNpc),
      });

      if (!response.ok) throw new Error('Failed to update NPC');
      
      const updatedNPC = await response.json();
      setNpc(updatedNPC);
      setEditedNpc(updatedNPC);
      setIsEditing(false);
      toast({
        title: 'Success',
        description: 'NPC updated successfully',
      });
    } catch (err) {
      toast({
        title: 'Error',
        description: 'Failed to update NPC',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  if (error) {
    return (
      <div className="container mx-auto p-4">
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      </div>
    );
  }

  if (!npc || !editedNpc) {
    return (
      <div className="container mx-auto p-4 space-y-4">
        <Skeleton className="h-8 w-1/3" />
        <Skeleton className="h-32 w-full" />
        <Skeleton className="h-32 w-full" />
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>{npc.name} - ARCANE NPC Profile</title>
        <meta name="description" content={`Profile page for ${npc.name}, a ${npc.race} ${npc.class}`} />
      </Head>

      <main className="container mx-auto p-4" role="main">
        <article className="space-y-6">
          <header className="flex justify-between items-center">
            <h1 className="text-3xl font-bold" id="npc-profile-title">
              {npc.name}
            </h1>
            <Button
              onClick={() => setIsEditing(!isEditing)}
              aria-label={isEditing ? 'Cancel editing' : 'Edit NPC'}
            >
              {isEditing ? 'Cancel' : 'Edit'}
            </Button>
          </header>

          <section aria-labelledby="basic-info-title">
            <h2 className="text-xl font-semibold mb-4" id="basic-info-title">Basic Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium mb-1">Name</label>
                <Input
                  id="name"
                  value={editedNpc.name}
                  onChange={(e) => handleOptimisticUpdate('name', e.target.value)}
                  disabled={!isEditing}
                  aria-label="NPC name"
                />
              </div>
              <div>
                <label htmlFor="race" className="block text-sm font-medium mb-1">Race</label>
                <Input
                  id="race"
                  value={editedNpc.race}
                  onChange={(e) => handleOptimisticUpdate('race', e.target.value)}
                  disabled={!isEditing}
                  aria-label="NPC race"
                />
              </div>
              <div>
                <label htmlFor="class" className="block text-sm font-medium mb-1">Class</label>
                <Input
                  id="class"
                  value={editedNpc.class}
                  onChange={(e) => handleOptimisticUpdate('class', e.target.value)}
                  disabled={!isEditing}
                  aria-label="NPC class"
                />
              </div>
            </div>
          </section>

          <section aria-labelledby="backstory-title">
            <h2 className="text-xl font-semibold mb-4" id="backstory-title">Backstory</h2>
            <div className="prose max-w-none">
              <ReactQuill
                value={editedNpc.backstory || ''}
                onChange={(content) => handleOptimisticUpdate('backstory', content)}
                readOnly={!isEditing}
                modules={{
                  toolbar: isEditing ? [
                    [{ 'header': [1, 2, 3, false] }],
                    ['bold', 'italic', 'underline'],
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    ['clean']
                  ] : false
                }}
              />
            </div>
          </section>

          {isEditing && (
            <div className="flex justify-end gap-4">
              <Button
                variant="outline"
                onClick={() => setIsEditing(false)}
                disabled={loading}
                aria-label="Cancel changes"
              >
                Cancel
              </Button>
              <Button
                onClick={handleSave}
                disabled={loading}
                aria-label="Save changes"
              >
                {loading ? 'Saving...' : 'Save Changes'}
              </Button>
            </div>
          )}
        </article>
      </main>
    </>
  );
};

export const getServerSideProps: GetServerSideProps<NPCProfileProps> = async ({ params, res }) => {
  try {
    await dbConnect();
    
    const id = params?.id;
    if (!id || typeof id !== 'string') {
      return { notFound: true };
    }

    const npc = await NPCModel.findById(id).lean();
    if (!npc) {
      return { notFound: true };
    }

    // Convert _id to string and prepare for client
    const serializedNPC = {
      ...npc,
      _id: npc._id.toString(),
      createdAt: npc.createdAt?.toISOString(),
      updatedAt: npc.updatedAt?.toISOString(),
    };

    return {
      props: {
        initialNPC: serializedNPC,
      },
    };
  } catch (error) {
    // Log error server-side for debugging
    console.error('Error fetching NPC:', error);
    
    // Set appropriate status code
    res.statusCode = 500;
    
    return {
      props: {
        initialNPC: null,
        error: 'Failed to load NPC data. Please try again later.',
      },
    };
  }
};

export default NPCProfile;
