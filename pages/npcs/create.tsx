import React from 'react';
import NPCForm from '../../components/NPCForm';

const CreateNPCPage = () => {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Create New NPC</h1>
      <NPCForm />
    </div>
  );
};

export default CreateNPCPage;
