/**
 * Formats a string value based on specified field type rules.
 * @param field - The type of field being formatted (e.g., 'Name', 'Race', 'Class', etc.)
 * @param response - The raw string value to be formatted
 * @returns The formatted string according to field-specific rules
 */
export const formatAIResponse = (field: string, response: string): string => {
  let formattedResponse = response.trim();

  // Helper function to capitalize each word in a string
  const capitalizeWords = (text: string): string =>
    text.split(' ').map(word => 
      word.split('-').map(part => 
        part.charAt(0).toUpperCase() + part.slice(1).toLowerCase()
      ).join('-')
    ).join(' ');

  switch (field.toLowerCase()) {
    // Character identification fields - capitalize each word
    case 'name':
    case 'race':
    case 'class':
      formattedResponse = capitalizeWords(formattedResponse);
      break;

    // Narrative fields - ensure proper sentence capitalization and punctuation
    case 'backstory':
    case 'personalitytraits':
    case 'appearance':
      formattedResponse = formattedResponse
        .split('. ')
        .map(sentence => sentence.charAt(0).toUpperCase() + sentence.slice(1))
        .join('. ')
        .trim();
      if (!formattedResponse.endsWith('.')) {
        formattedResponse += '.';
      }
      break;

    // Default case - return trimmed response without additional formatting
    default:
      break;
  }

  return formattedResponse;
};

/**
 * Interface defining the structure of monster data within an encounter
 */
interface Monster {
  name: string;
  stats?: any; // Consider defining a specific type for monster stats
}

/**
 * Interface for the main encounter component structure
 */
interface EncounterComponent {
  monsters: Monster[];
  // Add other encounter properties as needed
}

/**
 * Interface for encounter generation options
 */
interface GenerateEncounterOptions {
  // Define encounter generation options here
}

/**
 * Validates and enhances an encounter by:
 * 1. Validating the encounter content against predefined rules
 * 2. Fetching and attaching monster stats for each monster in the encounter
 * 
 * @param encounter - The encounter component to validate and enhance
 * @param options - Options for encounter generation
 * @returns Promise resolving to the enhanced encounter component
 * @throws Error if encounter content is invalid
 */
const validateAndEnhanceEncounter = async (
  encounter: EncounterComponent,
  options: GenerateEncounterOptions
): Promise<EncounterComponent> => {
  // Step 1: Validate encounter content
  const validationResult = await validateContent(encounter);
  if (!validationResult.isValid) {
    throw new Error(`Invalid encounter content: ${validationResult.errors.join(', ')}`);
  }

  // Step 2: Enhance monsters with their stats
  const enhancedMonsters = await Promise.all(
    encounter.monsters.map(async (monster) => {
      try {
        const stats = await fetchMonsterStats(monster.name);
        return { ...monster, stats };
      } catch (error) {
        console.warn(`Could not fetch stats for monster: ${monster.name}`);
        return monster;
      }
    })
  );

  return {
    ...encounter,
    monsters: enhancedMonsters
  };
};
