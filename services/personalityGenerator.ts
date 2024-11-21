interface PersonalityTraits {
  virtues: string[];
  flaws: string[];
  quirks: string[];
  ideals: string[];
  bonds: string[];
}

const personalityTraits: PersonalityTraits = {
  virtues: [
    'Courageous in the face of danger',
    'Fiercely loyal to allies',
    'Deeply compassionate',
    'Unwavering determination',
    'Quick-witted and clever',
    'Patient and methodical',
    'Natural leader',
    'Diplomatic mediator'
  ],
  flaws: [
    'Prone to rash decisions',
    'Struggles with trust',
    'Haunted by past failures',
    'Overly prideful',
    'Reluctant to accept help',
    'Quick to anger',
    'Holds grudges',
    'Overly suspicious'
  ],
  quirks: [
    'Always speaks in metaphors',
    'Collects unusual trinkets',
    'Whistles when nervous',
    'Quotes ancient texts',
    'Names their weapons',
    'Talks to animals',
    'Keeps detailed journals',
    'Never sits with back to door'
  ],
  ideals: [
    'Justice must prevail',
    'Knowledge is power',
    'Freedom above all',
    'Honor guides all actions',
    'Balance must be maintained',
    'Destiny shapes all',
    'Truth is sacred',
    'Protect the innocent'
  ],
  bonds: [
    'Sworn to protect their homeland',
    'Seeks to restore family honor',
    'Indebted to a mentor',
    'Guardian of ancient secrets',
    'Avenger of a fallen friend',
    'Keeper of a sacred oath',
    'Protector of the weak',
    'Servant of a higher power'
  ]
};

export interface PersonalityProfile {
  mainVirtue: string;
  mainFlaw: string;
  distinguishingQuirk: string;
  coreIdeal: string;
  primaryBond: string;
}

export function generatePersonality(prompt?: string): PersonalityProfile {
  // If a prompt is provided, use it to influence personality generation
  if (prompt) {
    // TODO: Implement more sophisticated prompt-based personality generation
    return {
      mainVirtue: prompt,
      mainFlaw: 'Determined by circumstance',
      distinguishingQuirk: 'Unique to their nature',
      coreIdeal: 'Shaped by experience',
      primaryBond: 'Forged through time'
    };
  }

  const getRandomElement = (arr: string[]) => arr[Math.floor(Math.random() * arr.length)];

  return {
    mainVirtue: getRandomElement(personalityTraits.virtues),
    mainFlaw: getRandomElement(personalityTraits.flaws),
    distinguishingQuirk: getRandomElement(personalityTraits.quirks),
    coreIdeal: getRandomElement(personalityTraits.ideals),
    primaryBond: getRandomElement(personalityTraits.bonds)
  };
}
