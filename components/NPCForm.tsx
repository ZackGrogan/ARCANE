import React, { useState } from 'react';
import axios from 'axios';

const NPCForm = () => {
  const [name, setName] = useState('');
  const [race, setRace] = useState('');
  const [characterClass, setCharacterClass] = useState('');
  const [background, setBackground] = useState('');
  const [alignment, setAlignment] = useState('');
  const [personalityTraits, setPersonalityTraits] = useState<string[]>([]);
  const [backstory, setBackstory] = useState('');
  const [appearance, setAppearance] = useState('');
  const [skills, setSkills] = useState<string[]>([]);
  const [equipment, setEquipment] = useState<string[]>([]);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    if (!name) newErrors.name = 'Name is required';
    if (!race) newErrors.race = 'Race is required';
    if (!characterClass) newErrors.class = 'Class is required';
    // Add more validations as needed
    return newErrors;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const formErrors = validateForm();
    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors);
      return;
    }
    try {
      const response = await axios.post('/api/npcs/create', {
        name,
        race,
        class: characterClass,
        background,
        alignment,
        personality_traits: personalityTraits,
        backstory,
        appearance,
        skills,
        equipment,
      });
      console.log('NPC created:', response.data);
      setErrors({}); // Clear errors on successful submission
    } catch (error) {
      console.error('Error creating NPC:', error);
    }
  };

  return (
    <div className="container mx-auto p-4 bg-white shadow-md rounded-md">
      <h1 className="text-3xl font-bold mb-6 text-center">Create New NPC</h1>
      <form onSubmit={handleSubmit} className="max-w-lg mx-auto p-6 bg-gray-50 rounded-md shadow-md">
        <div className="mb-4">
          <label htmlFor="name" className="block text-sm font-medium text-gray-700">
            Name
          </label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
          />
          {errors.name && <p className="text-red-500 text-xs mt-1">{errors.name}</p>}
        </div>
        <div className="mb-4">
          <label htmlFor="race" className="block text-sm font-medium text-gray-700">
            Race
          </label>
          <input
            type="text"
            id="race"
            value={race}
            onChange={(e) => setRace(e.target.value)}
            required
            className="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
          />
          {errors.race && <p className="text-red-500 text-xs mt-1">{errors.race}</p>}
        </div>
        <div className="mb-4">
          <label htmlFor="class" className="block text-sm font-medium text-gray-700">
            Class
          </label>
          <input
            type="text"
            id="class"
            value={characterClass}
            onChange={(e) => setCharacterClass(e.target.value)}
            required
            className="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
          />
          {errors.class && <p className="text-red-500 text-xs mt-1">{errors.class}</p>}
        </div>
        {/* Add more fields for background, alignment, personality traits, etc. */}
        <button type="submit" className="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Submit
        </button>
      </form>
    </div>
  );
};

export default NPCForm;
