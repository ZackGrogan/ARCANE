import { calculateDifficulty } from '@/utils/difficultyCalculator';

describe('difficultyCalculator', () => {
  const mockPartyInfo = {
    size: 4,
    averageLevel: 5,
  };

  describe('calculateDifficulty', () => {
    it('should calculate easy difficulty correctly', () => {
      const monsters = [
        {
          name: 'Goblin',
          quantity: 2,
          stats: {
            challenge_rating: 0.25,
            xp: 50,
          },
        },
      ];

      const difficulty = calculateDifficulty(monsters, mockPartyInfo);
      expect(difficulty).toBe('easy');
    });

    it('should calculate medium difficulty correctly', () => {
      const monsters = [
        {
          name: 'Dire Wolf',
          quantity: 2,
          stats: {
            challenge_rating: 1,
            xp: 200,
          },
        },
      ];

      const difficulty = calculateDifficulty(monsters, mockPartyInfo);
      expect(difficulty).toBe('medium');
    });

    it('should calculate hard difficulty correctly', () => {
      const monsters = [
        {
          name: 'Ogre',
          quantity: 2,
          stats: {
            challenge_rating: 2,
            xp: 450,
          },
        },
      ];

      const difficulty = calculateDifficulty(monsters, mockPartyInfo);
      expect(difficulty).toBe('hard');
    });

    it('should calculate deadly difficulty correctly', () => {
      const monsters = [
        {
          name: 'Young Green Dragon',
          quantity: 1,
          stats: {
            challenge_rating: 8,
            xp: 3900,
          },
        },
      ];

      const difficulty = calculateDifficulty(monsters, mockPartyInfo);
      expect(difficulty).toBe('deadly');
    });

    it('should apply correct multiplier for multiple monsters', () => {
      const monsters = [
        {
          name: 'Goblin',
          quantity: 8,
          stats: {
            challenge_rating: 0.25,
            xp: 50,
          },
        },
      ];

      // 8 goblins = 400 XP base, with 2.5x multiplier = 1000 XP
      const difficulty = calculateDifficulty(monsters, mockPartyInfo);
      expect(difficulty).toBe('hard');
    });

    it('should handle monsters without stats', () => {
      const monsters = [
        {
          name: 'Custom Monster',
          quantity: 1,
        },
      ];

      const difficulty = calculateDifficulty(monsters, mockPartyInfo);
      expect(difficulty).toBe('easy');
    });

    it('should handle mixed monster types', () => {
      const monsters = [
        {
          name: 'Goblin',
          quantity: 4,
          stats: {
            challenge_rating: 0.25,
            xp: 50,
          },
        },
        {
          name: 'Hobgoblin',
          quantity: 2,
          stats: {
            challenge_rating: 0.5,
            xp: 100,
          },
        },
      ];

      // 4 goblins (200 XP) + 2 hobgoblins (200 XP) = 400 XP base
      // With 6 monsters total = 2x multiplier = 800 XP
      const difficulty = calculateDifficulty(monsters, mockPartyInfo);
      expect(difficulty).toBe('medium');
    });

    it('should handle different party sizes', () => {
      const monsters = [
        {
          name: 'Ogre',
          quantity: 1,
          stats: {
            challenge_rating: 2,
            xp: 450,
          },
        },
      ];

      // Test with smaller party
      const smallParty = { ...mockPartyInfo, size: 2 };
      expect(calculateDifficulty(monsters, smallParty)).toBe('deadly');

      // Test with larger party
      const largeParty = { ...mockPartyInfo, size: 6 };
      expect(calculateDifficulty(monsters, largeParty)).toBe('medium');
    });

    it('should handle different party levels', () => {
      const monsters = [
        {
          name: 'Ogre',
          quantity: 1,
          stats: {
            challenge_rating: 2,
            xp: 450,
          },
        },
      ];

      // Test with lower level party
      const lowLevelParty = { ...mockPartyInfo, averageLevel: 2 };
      expect(calculateDifficulty(monsters, lowLevelParty)).toBe('deadly');

      // Test with higher level party
      const highLevelParty = { ...mockPartyInfo, averageLevel: 10 };
      expect(calculateDifficulty(monsters, highLevelParty)).toBe('easy');
    });

    it('should handle edge cases for party info', () => {
      const monsters = [
        {
          name: 'Goblin',
          quantity: 1,
          stats: {
            challenge_rating: 0.25,
            xp: 50,
          },
        },
      ];

      // Test with level below 1
      const invalidLowLevel = { size: 4, averageLevel: 0 };
      expect(calculateDifficulty(monsters, invalidLowLevel)).toBe('easy');

      // Test with level above 20
      const invalidHighLevel = { size: 4, averageLevel: 21 };
      expect(calculateDifficulty(monsters, invalidHighLevel)).toBe('easy');
    });

    it('should handle extreme monster quantities', () => {
      const monsters = [
        {
          name: 'Goblin',
          quantity: 20,
          stats: {
            challenge_rating: 0.25,
            xp: 50,
          },
        },
      ];

      // 20 goblins = 1000 XP base, with 4x multiplier = 4000 XP
      const difficulty = calculateDifficulty(monsters, mockPartyInfo);
      expect(difficulty).toBe('deadly');
    });
  });
});
