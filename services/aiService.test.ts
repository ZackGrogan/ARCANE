import { aiGenerator } from './aiService';

describe('AIContentGenerator', () => {
  let generator: aiGenerator;

  beforeEach(() => {
    generator = new aiGenerator();
  });

  it('should generate a name', async () => {
    const name = await generator.generateName();
    expect(name).toBe('John Doe');
  });

  it('should generate a race', async () => {
    const race = await generator.generateRace();
    expect(race).toBe('Human');
  });

  it('should generate a class', async () => {
    const characterClass = await generator.generateClass();
    expect(characterClass).toBe('Warrior');
  });

  it('should generate a backstory', async () => {
    const backstory = await generator.generateBackstory();
    expect(backstory).toBe('A brave warrior from the northern lands.');
  });

  it('should generate personality traits', async () => {
    const personalityTraits = await generator.generatePersonalityTraits();
    expect(personalityTraits).toBe('Brave, Loyal, Strong');
  });

  it('should generate an appearance', async () => {
    const appearance = await generator.generateAppearance();
    expect(appearance).toBe('Tall with a muscular build and a scar across his face.');
  });
});
