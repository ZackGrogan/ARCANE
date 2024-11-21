import { validateContent } from '@/utils/contentValidator';

describe('contentValidator', () => {
  const validEncounter = {
    title: 'Test Encounter',
    description: 'This is a valid encounter description that meets the minimum length requirement for testing purposes.',
    monsters: [
      {
        name: 'Goblin',
        quantity: 3,
      },
      {
        name: 'Hobgoblin',
        quantity: 1,
      },
    ],
    tactics: ['Goblins attack from range', 'Hobgoblin engages in melee'],
    biome: 'Forest',
    weather: 'Cloudy',
    hazards: ['Difficult terrain'],
    loot: [
      {
        item: 'Gold coins',
        rarity: 'Common',
        quantity: 50,
      },
    ],
    roleplayingScenarios: [
      'The goblins are willing to negotiate if approached peacefully.',
    ],
    difficulty: 'medium',
    environmentDetails: {
      terrain: 'Dense forest',
      lighting: 'Dim light',
      specialFeatures: ['Fallen trees', 'Small stream'],
    },
  };

  describe('required fields validation', () => {
    it('should validate a correct encounter', async () => {
      const result = await validateContent(validEncounter);
      expect(result.isValid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should detect missing required fields', async () => {
      const invalidEncounter = { ...validEncounter };
      delete invalidEncounter.description;
      delete invalidEncounter.monsters;

      const result = await validateContent(invalidEncounter);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Missing required field: description');
      expect(result.errors).toContain('Missing required field: monsters');
    });
  });

  describe('description length validation', () => {
    it('should validate correct description length', async () => {
      const result = await validateContent(validEncounter);
      expect(result.isValid).toBe(true);
    });

    it('should detect too short description', async () => {
      const shortEncounter = {
        ...validEncounter,
        description: 'Too short',
      };

      const result = await validateContent(shortEncounter);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Description too short (minimum 50 characters)');
    });

    it('should detect too long description', async () => {
      const longEncounter = {
        ...validEncounter,
        description: 'a'.repeat(2001),
      };

      const result = await validateContent(longEncounter);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Description too long (maximum 2000 characters)');
    });
  });

  describe('monster validation', () => {
    it('should validate correct monster entries', async () => {
      const result = await validateContent(validEncounter);
      expect(result.isValid).toBe(true);
    });

    it('should detect invalid monster quantity', async () => {
      const invalidMonsterEncounter = {
        ...validEncounter,
        monsters: [
          {
            name: 'Goblin',
            quantity: 0,
          },
        ],
      };

      const result = await validateContent(invalidMonsterEncounter);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Invalid monster quantity for Goblin');
    });

    it('should detect too many monsters', async () => {
      const tooManyMonsters = {
        ...validEncounter,
        monsters: Array(11).fill({ name: 'Goblin', quantity: 1 }),
      };

      const result = await validateContent(tooManyMonsters);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Too many monsters (maximum 10)');
    });
  });

  describe('loot validation', () => {
    it('should validate correct loot entries', async () => {
      const result = await validateContent(validEncounter);
      expect(result.isValid).toBe(true);
    });

    it('should detect invalid loot entries', async () => {
      const invalidLootEncounter = {
        ...validEncounter,
        loot: [
          {
            item: '',
            rarity: 'Common',
            quantity: 1,
          },
          {
            item: 'Potion',
            rarity: '',
            quantity: 0,
          },
        ],
      };

      const result = await validateContent(invalidLootEncounter);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Invalid loot: missing or invalid item name');
      expect(result.errors).toContain('Invalid loot: missing or invalid rarity');
      expect(result.errors).toContain('Invalid loot quantity for Potion');
    });
  });

  describe('environment validation', () => {
    it('should validate correct environment details', async () => {
      const result = await validateContent(validEncounter);
      expect(result.isValid).toBe(true);
    });

    it('should detect invalid environment details', async () => {
      const invalidEnvironmentEncounter = {
        ...validEncounter,
        environmentDetails: {
          terrain: '',
          lighting: '',
          specialFeatures: 'not an array',
        },
      };

      const result = await validateContent(invalidEnvironmentEncounter);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Invalid environment: missing or invalid terrain');
      expect(result.errors).toContain('Invalid environment: missing or invalid lighting');
      expect(result.errors).toContain('Invalid environment: special features must be an array');
    });
  });

  describe('roleplaying scenarios validation', () => {
    it('should validate correct roleplaying scenarios', async () => {
      const result = await validateContent(validEncounter);
      expect(result.isValid).toBe(true);
    });

    it('should detect invalid roleplaying scenarios', async () => {
      const invalidRoleplayEncounter = {
        ...validEncounter,
        roleplayingScenarios: ['Too short'],
      };

      const result = await validateContent(invalidRoleplayEncounter);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Invalid roleplaying scenario: too short or invalid format');
    });

    it('should detect missing roleplaying scenarios', async () => {
      const noRoleplayEncounter = {
        ...validEncounter,
        roleplayingScenarios: [],
      };

      const result = await validateContent(noRoleplayEncounter);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('At least one roleplaying scenario is required');
    });
  });

  describe('difficulty validation', () => {
    it('should validate correct difficulty levels', async () => {
      const validDifficulties = ['easy', 'medium', 'hard', 'deadly'];

      for (const difficulty of validDifficulties) {
        const encounter = { ...validEncounter, difficulty };
        const result = await validateContent(encounter);
        expect(result.isValid).toBe(true);
      }
    });

    it('should detect invalid difficulty levels', async () => {
      const invalidDifficulties = ['invalid', 'very hard', ''];

      for (const difficulty of invalidDifficulties) {
        const encounter = { ...validEncounter, difficulty };
        const result = await validateContent(encounter);
        expect(result.isValid).toBe(false);
        expect(result.errors).toContain('Invalid difficulty level');
      }
    });

    it('should detect invalid data format', async () => {
      const invalidEncounter = { ...validEncounter, difficulty: 123 };
      const result = await validateContent(invalidEncounter);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Invalid difficulty format');
    });
  });

  describe('custom rules', () => {
    it('should apply custom validation rules', async () => {
      const customRules = {
        minLength: 100,
        maxLength: 500,
        maxMonsters: 5,
        bannedWords: ['dragon'],
      };

      const validCustomEncounter = {
        ...validEncounter,
        description: 'a'.repeat(200),
      };

      const result = await validateContent(validCustomEncounter, customRules);
      expect(result.isValid).toBe(true);
    });

    it('should detect violations of custom rules', async () => {
      const customRules = {
        minLength: 100,
        maxLength: 500,
        maxMonsters: 5,
        bannedWords: ['goblin'],
      };

      const result = await validateContent(validEncounter, customRules);
      expect(result.isValid).toBe(false);
      expect(result.errors).toContain('Description too short (minimum 100 characters)');
      expect(result.errors).toContain('Content contains inappropriate word: goblin');
    });
  });
});

jest.mock('@/utils/externalDependency', () => ({
  externalFunction: jest.fn().mockReturnValue(true)
}));
