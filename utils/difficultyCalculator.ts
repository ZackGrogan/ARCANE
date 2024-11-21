interface PartyInfo {
  size: number;
  averageLevel: number;
}

interface Monster {
  name: string;
  quantity: number;
  stats?: {
    challenge_rating: number;
    xp: number;
  };
}

interface EncounterDifficulty {
  easy: number;
  medium: number;
  hard: number;
  deadly: number;
}

// XP Thresholds by Character Level (D&D 5e DMG p.82)
const XP_THRESHOLDS: { [key: number]: EncounterDifficulty } = {
  1: { easy: 25, medium: 50, hard: 75, deadly: 100 },
  2: { easy: 50, medium: 100, hard: 150, deadly: 200 },
  3: { easy: 75, medium: 150, hard: 225, deadly: 400 },
  4: { easy: 125, medium: 250, hard: 375, deadly: 500 },
  5: { easy: 250, medium: 500, hard: 750, deadly: 1100 },
  6: { easy: 300, medium: 600, hard: 900, deadly: 1400 },
  7: { easy: 350, medium: 750, hard: 1100, deadly: 1700 },
  8: { easy: 450, medium: 900, hard: 1400, deadly: 2100 },
  9: { easy: 550, medium: 1100, hard: 1600, deadly: 2400 },
  10: { easy: 600, medium: 1200, hard: 1900, deadly: 2800 },
  11: { easy: 800, medium: 1600, hard: 2400, deadly: 3600 },
  12: { easy: 1000, medium: 2000, hard: 3000, deadly: 4500 },
  13: { easy: 1100, medium: 2200, hard: 3400, deadly: 5100 },
  14: { easy: 1250, medium: 2500, hard: 3800, deadly: 5700 },
  15: { easy: 1400, medium: 2800, hard: 4300, deadly: 6400 },
  16: { easy: 1600, medium: 3200, hard: 4800, deadly: 7200 },
  17: { easy: 2000, medium: 3900, hard: 5900, deadly: 8800 },
  18: { easy: 2100, medium: 4200, hard: 6300, deadly: 9500 },
  19: { easy: 2400, medium: 4900, hard: 7300, deadly: 10900 },
  20: { easy: 2800, medium: 5700, hard: 8500, deadly: 12700 }
};

// Multipliers for multiple monsters (D&D 5e DMG p.82)
const MONSTER_MULTIPLIERS = [
  { count: 1, multiplier: 1 },
  { count: 2, multiplier: 1.5 },
  { count: 3, multiplier: 2 },
  { count: 7, multiplier: 2.5 },
  { count: 11, multiplier: 3 },
  { count: 15, multiplier: 4 }
];

export const calculateDifficulty = (
  monsters: Monster[],
  partyInfo: PartyInfo
): string => {
  // Calculate total XP from monsters
  let totalXP = monsters.reduce((sum, monster) => {
    const xp = monster.stats?.xp || getEstimatedXP(monster.stats?.challenge_rating || 0);
    return sum + (xp * monster.quantity);
  }, 0);

  // Apply multiplier based on number of monsters
  const totalMonsters = monsters.reduce((sum, monster) => sum + monster.quantity, 0);
  const multiplier = getMonsterMultiplier(totalMonsters);
  const adjustedXP = totalXP * multiplier;

  // Get party thresholds
  const partyThresholds = calculatePartyThresholds(partyInfo);

  // Determine difficulty
  if (adjustedXP < partyThresholds.easy) return 'easy';
  if (adjustedXP < partyThresholds.medium) return 'medium';
  if (adjustedXP < partyThresholds.hard) return 'hard';
  return 'deadly';
};

const getEstimatedXP = (cr: number): number => {
  const xpByCR: { [key: number]: number } = {
    0: 10, 0.125: 25, 0.25: 50, 0.5: 100, 1: 200,
    2: 450, 3: 700, 4: 1100, 5: 1800, 6: 2300,
    7: 2900, 8: 3900, 9: 5000, 10: 5900, 11: 7200,
    12: 8400, 13: 10000, 14: 11500, 15: 13000, 16: 15000,
    17: 18000, 18: 20000, 19: 22000, 20: 25000, 21: 33000,
    22: 41000, 23: 50000, 24: 62000, 25: 75000, 26: 90000,
    27: 105000, 28: 120000, 29: 135000, 30: 155000
  };

  return xpByCR[cr] || 0;
};

const getMonsterMultiplier = (monsterCount: number): number => {
  const multiplierInfo = MONSTER_MULTIPLIERS
    .slice()
    .reverse()
    .find(m => monsterCount >= m.count);

  return multiplierInfo?.multiplier || 4;
};

const calculatePartyThresholds = (partyInfo: PartyInfo): EncounterDifficulty => {
  const level = Math.min(Math.max(Math.round(partyInfo.averageLevel), 1), 20);
  const levelThresholds = XP_THRESHOLDS[level];

  return {
    easy: levelThresholds.easy * partyInfo.size,
    medium: levelThresholds.medium * partyInfo.size,
    hard: levelThresholds.hard * partyInfo.size,
    deadly: levelThresholds.deadly * partyInfo.size
  };
};
