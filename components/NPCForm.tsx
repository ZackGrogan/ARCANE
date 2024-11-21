import React, { useState } from 'react';
import axios from 'axios';
import { aiGenerator } from '../services/aiService';
import { useForm } from 'react-hook-form';
import AIGenerationModal from './AIGenerationModal';

interface NPCFormData {
  name: string;
  race: string;
  class: string;
  backstory: string;
  personalityTraits: string;
  appearance: string;
  background: string;
  alignment: string;
  skills: string;
  equipment: string;
}

const NPCForm = () => {
  const { register, handleSubmit, setValue, watch } = useForm<NPCFormData>();
  const [selectedField, setSelectedField] = useState<keyof NPCFormData | null>(null);
  const currentValues = watch();

  const handleAIGenerate = (field: keyof NPCFormData) => {
    setSelectedField(field);
  };

  const handleGeneratedContent = (content: string) => {
    if (selectedField) {
      setValue(selectedField, content);
    }
    setSelectedField(null);
  };

  const renderAIButton = (field: keyof NPCFormData) => (
    <button
      type="button"
      onClick={() => handleAIGenerate(field)}
      className="inline-flex items-center px-2 py-1 text-sm font-medium text-indigo-600 bg-indigo-100 rounded hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
    >
      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
      </svg>
      AI Generate
    </button>
  );

  const onSubmit = async (data: NPCFormData) => {
    try {
      const response = await axios.post('/api/npcs/create', {
        name: data.name,
        race: data.race,
        class: data.class,
        background: data.background,
        alignment: data.alignment,
        personality_traits: data.personalityTraits,
        backstory: data.backstory,
        appearance: data.appearance,
        skills: data.skills,
        equipment: data.equipment,
      });
      console.log('NPC created:', response.data);
    } catch (error) {
      console.error('Error creating NPC:', error);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700">Name</label>
          <div className="mt-1 flex items-center gap-2">
            <input
              type="text"
              id="name"
              {...register('name')}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
            {renderAIButton('name')}
          </div>
        </div>

        <div>
          <label htmlFor="race" className="block text-sm font-medium text-gray-700">Race</label>
          <div className="mt-1 flex items-center gap-2">
            <input
              type="text"
              id="race"
              {...register('race')}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
            {renderAIButton('race')}
          </div>
        </div>

        <div>
          <label htmlFor="class" className="block text-sm font-medium text-gray-700">Class</label>
          <div className="mt-1 flex items-center gap-2">
            <input
              type="text"
              id="class"
              {...register('class')}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
            {renderAIButton('class')}
          </div>
        </div>

        <div>
          <label htmlFor="backstory" className="block text-sm font-medium text-gray-700">Backstory</label>
          <div className="mt-1 flex items-start gap-2">
            <textarea
              id="backstory"
              rows={4}
              {...register('backstory')}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
            {renderAIButton('backstory')}
          </div>
        </div>

        <div>
          <label htmlFor="personalityTraits" className="block text-sm font-medium text-gray-700">Personality Traits</label>
          <div className="mt-1 flex items-start gap-2">
            <textarea
              id="personalityTraits"
              rows={4}
              {...register('personalityTraits')}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
            {renderAIButton('personalityTraits')}
          </div>
        </div>

        <div>
          <label htmlFor="appearance" className="block text-sm font-medium text-gray-700">Appearance</label>
          <div className="mt-1 flex items-start gap-2">
            <textarea
              id="appearance"
              rows={4}
              {...register('appearance')}
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            />
            {renderAIButton('appearance')}
          </div>
        </div>

        <div>
          <label htmlFor="background" className="block text-sm font-medium text-gray-700">Background</label>
          <input
            type="text"
            id="background"
            {...register('background')}
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        <div>
          <label htmlFor="alignment" className="block text-sm font-medium text-gray-700">Alignment</label>
          <input
            type="text"
            id="alignment"
            {...register('alignment')}
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        <div>
          <label htmlFor="skills" className="block text-sm font-medium text-gray-700">Skills</label>
          <input
            type="text"
            id="skills"
            {...register('skills')}
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        <div>
          <label htmlFor="equipment" className="block text-sm font-medium text-gray-700">Equipment</label>
          <input
            type="text"
            id="equipment"
            {...register('equipment')}
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          />
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            className="inline-flex justify-center rounded-md border border-transparent bg-indigo-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            Save NPC
          </button>
        </div>
      </form>

      {selectedField && (
        <AIGenerationModal
          isOpen={true}
          onClose={() => setSelectedField(null)}
          field={selectedField}
          currentCharacter={currentValues}
          onGenerate={handleGeneratedContent}
        />
      )}
    </div>
  );
};

export default NPCForm;
