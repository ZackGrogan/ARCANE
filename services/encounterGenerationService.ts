import axios from 'axios';
import { validateContent } from '@/utils/contentValidator';
import { calculateDifficulty } from '@/utils/difficultyCalculator';

interface PartyInfo {
  size: number;
  averageLevel: number;
}

interface EncounterModifiers {
  environment?: string;
  theme?: string;
  constraints?: string[];
}

interface EncounterComponent {
  title: string;
  description: string;
  monsters: Array<{
    name: string;
    quantity: number;
    stats?: any;
  }>;
  tactics: string[];
  biome: string;
  weather: string;
  hazards: string[];
  loot: Array<{
    item: string;
    rarity: string;
    quantity: number;
  }>;
  roleplayingScenarios: string[];
  difficulty: string;
  tacticalMap?: string;
  environmentDetails: {
    terrain: string;
    lighting: string;
    specialFeatures: string[];
  };
}

interface GenerateEncounterOptions {
  partyInfo: PartyInfo;
  modifiers?: EncounterModifiers;
  quickGenerate?: boolean;
}

const AI_API_URL = process.env.NEXT_PUBLIC_AI_API_URL;
const DND5E_API_URL = 'https://www.dnd5eapi.co/api';

if (!AI_API_URL) {
  throw new Error('AI_API_URL is not defined in the environment variables.');
}

const MAX_RETRIES = 3;
const TIMEOUT_MS = 10000;

export const generateEncounter = async (
  prompt: string,
  options: GenerateEncounterOptions,
  retryCount = 0
): Promise<EncounterComponent> => {
  try {
    // Build the enhanced prompt
    const enhancedPrompt = buildPrompt(prompt, options);
    
    // Generate the initial encounter
    const response = await axios.post(AI_API_URL, 
      { prompt: enhancedPrompt },
      { 
        timeout: TIMEOUT_MS,
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

    // Validate response
    if (!response.data || typeof response.data !== 'object') {
      throw new Error('Invalid response format');
    }

    // Validate and enhance the generated content
    let encounter = await validateAndEnhanceEncounter(response.data, options);

    // Calculate and verify difficulty
    encounter = await verifyDifficulty(encounter, options.partyInfo);

    return encounter;
  } catch (error) {
    if (retryCount < MAX_RETRIES && error.code === 'ECONNABORTED') {
      console.warn(`Retry attempt ${retryCount + 1} for encounter generation`);
      return generateEncounter(prompt, options, retryCount + 1);
    }
    console.error('Error generating encounter:', {
      error,
      prompt,
      options,
    });
    throw error;
  }
};

const buildPrompt = (basePrompt: string, options: GenerateEncounterOptions): string => {
  const { partyInfo, modifiers } = options;
  
  let prompt = `Create a D&D 5e encounter that is appropriate for ${partyInfo.size} level ${partyInfo.averageLevel} players.\n`;
  prompt += `Base concept: ${basePrompt}\n`;

  if (modifiers) {
    if (modifiers.environment) {
      prompt += `Environment: ${modifiers.environment}\n`;
    }
    if (modifiers.theme) {
      prompt += `Theme: ${modifiers.theme}\n`;
    }
    if (modifiers.constraints?.length) {
      prompt += `Additional requirements: ${modifiers.constraints.join(', ')}\n`;
    }
  }

  return prompt;
};

const validateAndEnhanceEncounter = async (
  encounter: EncounterComponent,
  options: GenerateEncounterOptions
): Promise<EncounterComponent> => {
  // Content validation
  const validationResult = await validateContent(encounter);
  if (!validationResult.isValid) {
    throw new Error(`Invalid encounter content: ${validationResult.errors.join(', ')}`);
  }

  // Enhance with monster stats
  for (let i = 0; i < encounter.monsters.length; i++) {
    const monster = encounter.monsters[i];
    try {
      const stats = await fetchMonsterStats(monster.name);
      encounter.monsters[i] = { ...monster, stats };
    } catch (error) {
      console.warn(`Could not fetch stats for monster: ${monster.name}`);
    }
  }

  return encounter;
};

const verifyDifficulty = async (
  encounter: EncounterComponent,
  partyInfo: PartyInfo
): Promise<EncounterComponent> => {
  const calculatedDifficulty = calculateDifficulty(encounter.monsters, partyInfo);
  
  // Adjust encounter if difficulty doesn't match
  if (calculatedDifficulty !== encounter.difficulty) {
    encounter.difficulty = calculatedDifficulty;
  }

  return encounter;
};

const fetchMonsterStats = async (monsterName: string): Promise<any> => {
  try {
    const formattedName = monsterName.toLowerCase().replace(/\s+/g, '-');
    const response = await axios.get(`${DND5E_API_URL}/monsters/${formattedName}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching stats for monster ${monsterName}:`, error);
    return null;
  }
};
