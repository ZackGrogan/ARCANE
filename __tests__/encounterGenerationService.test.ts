import { generateEncounter } from '../services/encounterGenerationService';

jest.mock('axios', () => ({
  post: jest.fn().mockImplementation((url, { prompt }) => {
    if (prompt.includes('desert')) {
      return Promise.resolve({
        status: 200,
        data: {
          title: 'Desert Bandit Raid',
          description: 'Bandits raid the party in the scorching desert.',
          monsters: ['Bandit', 'Bandit Leader'],
          biome: 'Desert',
          difficulty: 'Hard',
        },
      });
    } else if (prompt.includes('forest')) {
      return Promise.resolve({
        status: 200,
        data: {
          title: 'Goblin Ambush',
          description: 'A group of goblins ambush the party on a narrow forest path.',
          monsters: ['Goblin', 'Goblin Boss'],
          tactics: ['Ambush', 'Hit and Run'],
          biome: 'Forest',
          weather: 'Overcast',
          hazards: ['Falling Branches'],
          loot: ['Gold Coins', 'Potion of Healing'],
          roleplayingScenarios: ['Negotiate with Goblin Leader'],
          difficulty: 'Medium',
        },
      });
    }
    return Promise.reject(new Error('Unsupported environment'));
  }),
}));

describe('Encounter Generation Service', () => {
  it('should generate an encounter with valid components', async () => {
    const prompt = 'Generate a forest encounter with goblins';
    const encounter = await generateEncounter(prompt);
    expect(encounter.title).toBe('Goblin Ambush');
    expect(encounter.monsters).toContain('Goblin');
    expect(encounter.difficulty).toBe('Medium');
  });

  it('should handle errors gracefully', async () => {
    (axios.post as jest.Mock).mockRejectedValueOnce(new Error('API Error'));
    const prompt = 'Generate a desert encounter with bandits';
    await expect(generateEncounter(prompt)).rejects.toThrow('Error generating encounter');
  });

  it('should generate an encounter in a desert environment', async () => {
    const prompt = 'Generate a desert encounter with bandits';
    const encounter = await generateEncounter(prompt);
    expect(encounter.biome).toBe('Desert');
    expect(encounter.monsters).toContain('Bandit');
  });
});
