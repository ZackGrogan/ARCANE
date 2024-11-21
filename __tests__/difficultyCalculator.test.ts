import { calculateEncounterDifficulty } from '../utils/difficultyCalculator';

describe('Difficulty Calculator', () => {
  it('should return Trivial for very low XP encounters', () => {
    const party = [{ level: 3 }, { level: 3 }, { level: 3 }];
    const encounterXP = 10;
    const difficulty = calculateEncounterDifficulty(party, encounterXP);
    expect(difficulty).toBe('Trivial');
  });

  it('should return Easy for low XP encounters', () => {
    const party = [{ level: 3 }, { level: 3 }, { level: 3 }];
    const encounterXP = 50;
    const difficulty = calculateEncounterDifficulty(party, encounterXP);
    expect(difficulty).toBe('Easy');
  });

  it('should return Medium for moderate XP encounters', () => {
    const party = [{ level: 3 }, { level: 3 }, { level: 3 }];
    const encounterXP = 150;
    const difficulty = calculateEncounterDifficulty(party, encounterXP);
    expect(difficulty).toBe('Medium');
  });

  it('should return Hard for high XP encounters', () => {
    const party = [{ level: 3 }, { level: 3 }, { level: 3 }];
    const encounterXP = 250;
    const difficulty = calculateEncounterDifficulty(party, encounterXP);
    expect(difficulty).toBe('Hard');
  });

  it('should return Deadly for very high XP encounters', () => {
    const party = [{ level: 3 }, { level: 3 }, { level: 3 }];
    const encounterXP = 400;
    const difficulty = calculateEncounterDifficulty(party, encounterXP);
    expect(difficulty).toBe('Deadly');
  });
});
