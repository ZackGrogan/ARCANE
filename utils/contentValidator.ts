interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

interface ContentRules {
  minLength: number;
  maxLength: number;
  requiredFields: string[];
  bannedWords: string[];
  maxMonsters: number;
}

const DEFAULT_RULES: ContentRules = {
  minLength: 50,
  maxLength: 2000,
  requiredFields: ['title', 'description', 'monsters', 'tactics'],
  bannedWords: [
    // Add inappropriate or banned words here
  ],
  maxMonsters: 10,
};

export const validateContent = async (
  content: any,
  rules: Partial<ContentRules> = {}
): Promise<ValidationResult> => {
  const finalRules = { ...DEFAULT_RULES, ...rules };
  const errors: string[] = [];

  // Check required fields
  for (const field of finalRules.requiredFields) {
    if (!content[field]) {
      errors.push(`Missing required field: ${field}`);
    }
  }

  // Validate description length
  if (content.description) {
    if (content.description.length < finalRules.minLength) {
      errors.push(`Description too short (minimum ${finalRules.minLength} characters)`);
    }
    if (content.description.length > finalRules.maxLength) {
      errors.push(`Description too long (maximum ${finalRules.maxLength} characters)`);
    }
  }

  // Check for banned words
  const contentString = JSON.stringify(content).toLowerCase();
  for (const word of finalRules.bannedWords) {
    if (contentString.includes(word.toLowerCase())) {
      errors.push(`Content contains inappropriate word: ${word}`);
    }
  }

  // Validate monsters
  if (content.monsters && Array.isArray(content.monsters)) {
    if (content.monsters.length > finalRules.maxMonsters) {
      errors.push(`Too many monsters (maximum ${finalRules.maxMonsters})`);
    }

    // Validate each monster
    for (const monster of content.monsters) {
      if (!monster.name || typeof monster.name !== 'string') {
        errors.push('Invalid monster: missing or invalid name');
      }
      if (!monster.quantity || typeof monster.quantity !== 'number' || monster.quantity < 1) {
        errors.push(`Invalid monster quantity for ${monster.name}`);
      }
    }
  }

  // Validate loot
  if (content.loot && Array.isArray(content.loot)) {
    for (const item of content.loot) {
      if (!item.item || typeof item.item !== 'string') {
        errors.push('Invalid loot: missing or invalid item name');
      }
      if (!item.rarity || typeof item.rarity !== 'string') {
        errors.push(`Invalid loot rarity for ${item.item}`);
      }
      if (!item.quantity || typeof item.quantity !== 'number' || item.quantity < 1) {
        errors.push(`Invalid loot quantity for ${item.item}`);
      }
    }
  }

  // Validate environment details
  if (content.environmentDetails) {
    const { terrain, lighting, specialFeatures } = content.environmentDetails;
    if (!terrain || typeof terrain !== 'string') {
      errors.push('Invalid environment: missing or invalid terrain');
    }
    if (!lighting || typeof lighting !== 'string') {
      errors.push('Invalid environment: missing or invalid lighting');
    }
    if (!Array.isArray(specialFeatures)) {
      errors.push('Invalid environment: special features must be an array');
    }
  }

  // Validate roleplay scenarios
  if (content.roleplayingScenarios && Array.isArray(content.roleplayingScenarios)) {
    if (content.roleplayingScenarios.length === 0) {
      errors.push('At least one roleplaying scenario is required');
    }
    for (const scenario of content.roleplayingScenarios) {
      if (typeof scenario !== 'string' || scenario.length < 20) {
        errors.push('Invalid roleplaying scenario: too short or invalid format');
      }
    }
  }

  // Validate difficulty
  if (!['easy', 'medium', 'hard', 'deadly'].includes(content.difficulty?.toLowerCase())) {
    errors.push('Invalid difficulty level');
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
};
