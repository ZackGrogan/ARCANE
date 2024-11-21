import { generateEncounter } from '@/services/encounterGenerationService';
import axios from 'axios';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('encounterGenerationService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  const mockPartyInfo = {
    size: 4,
    averageLevel: 5,
  };

  const mockModifiers = {
    environment: 'Forest',
    theme: 'Mystery',
    constraints: ['No undead'],
  };

  const mockEncounterResponse = {
    title: 'The Whispering Grove',
    description: 'A mysterious encounter in a dark forest...',
    monsters: [
      {
        name: 'Dire Wolf',
        quantity: 2,
        stats: {
          challenge_rating: 1,
          xp: 200,
        },
      },
    ],
    tactics: ['Wolves attack from different directions'],
    biome: 'Forest',
    weather: 'Foggy',
    hazards: ['Difficult terrain', 'Limited visibility'],
    loot: [
      {
        item: 'Potion of Healing',
        rarity: 'Common',
        quantity: 1,
      },
    ],
    roleplayingScenarios: ['The wolves are protecting their cubs'],
    difficulty: 'medium',
    environmentDetails: {
      terrain: 'Dense forest',
      lighting: 'Dim light',
      specialFeatures: ['Ancient trees', 'Fog banks'],
    },
  };

  describe('generateEncounter', () => {
    it('should generate an encounter with quick options', async () => {
      mockedAxios.post.mockResolvedValueOnce({ status: 200, data: mockEncounterResponse });

      const result = await generateEncounter('A forest encounter', {
        partyInfo: mockPartyInfo,
        quickGenerate: true,
      });

      expect(result).toEqual(mockEncounterResponse);
      expect(mockedAxios.post).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          prompt: expect.stringContaining('forest encounter'),
        })
      );
    });

    it('should generate an encounter with advanced options', async () => {
      mockedAxios.post.mockResolvedValueOnce({ status: 200, data: mockEncounterResponse });

      const result = await generateEncounter('A forest encounter', {
        partyInfo: mockPartyInfo,
        modifiers: mockModifiers,
      });

      expect(result).toEqual(mockEncounterResponse);
      expect(mockedAxios.post).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          prompt: expect.stringContaining('Forest'),
        })
      );
    });

    it('should handle API errors gracefully', async () => {
      mockedAxios.post.mockRejectedValueOnce(new Error('API Error'));

      await expect(
        generateEncounter('A forest encounter', {
          partyInfo: mockPartyInfo,
        })
      ).rejects.toThrow('API Error');
    });

    it('should handle non-200 status codes', async () => {
      mockedAxios.post.mockResolvedValueOnce({
        status: 400,
        statusText: 'Bad Request',
      });

      await expect(
        generateEncounter('A forest encounter', {
          partyInfo: mockPartyInfo,
        })
      ).rejects.toThrow('Failed to generate encounter: Bad Request');
    });

    it('should validate monster stats are fetched', async () => {
      const encounterWithoutStats = {
        ...mockEncounterResponse,
        monsters: [{ name: 'Dire Wolf', quantity: 2 }],
      };

      mockedAxios.post.mockResolvedValueOnce({
        status: 200,
        data: encounterWithoutStats,
      });

      mockedAxios.get.mockResolvedValueOnce({
        data: { challenge_rating: 1, xp: 200 },
      });

      const result = await generateEncounter('A forest encounter', {
        partyInfo: mockPartyInfo,
      });

      expect(result.monsters[0].stats).toEqual({
        challenge_rating: 1,
        xp: 200,
      });
    });

    it('should handle missing monster stats gracefully', async () => {
      const encounterWithoutStats = {
        ...mockEncounterResponse,
        monsters: [{ name: 'Unknown Monster', quantity: 1 }],
      };

      mockedAxios.post.mockResolvedValueOnce({
        status: 200,
        data: encounterWithoutStats,
      });

      mockedAxios.get.mockRejectedValueOnce(new Error('Monster not found'));

      const result = await generateEncounter('A forest encounter', {
        partyInfo: mockPartyInfo,
      });

      expect(result.monsters[0].stats).toBeNull();
    });
  });
});
