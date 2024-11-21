interface PhysicalTraits {
  height: string[];
  build: string[];
  complexion: string[];
  eyes: string[];
  hair: string[];
  distinguishingFeatures: string[];
  clothing: string[];
}

const physicalTraits: PhysicalTraits = {
  height: [
    'Towering and imposing',
    'Tall and graceful',
    'Average height but commanding',
    'Compact and agile',
    'Short but sturdy'
  ],
  build: [
    'Muscular and athletic',
    'Lean and wiry',
    'Broad and powerful',
    'Slender and elegant',
    'Stocky and robust'
  ],
  complexion: [
    'Fair with rosy undertones',
    'Deep bronze with a healthy glow',
    'Pale and ethereal',
    'Rich ebony',
    'Sun-kissed golden'
  ],
  eyes: [
    'Piercing {color} that seem to glow',
    'Deep, thoughtful {color}',
    'Bright, alert {color}',
    'Mysterious, shifting {color}',
    'Gentle, kind {color}'
  ],
  hair: [
    'Long, flowing {color} locks',
    'Short, neat {color} style',
    'Wild, untamed {color} mane',
    'Braided {color} strands',
    'Shaved/bald with {color} stubble'
  ],
  distinguishingFeatures: [
    'Intricate tribal tattoos',
    'Battle scars that tell stories',
    'Unusual birthmark',
    'Ritual markings',
    'Ethereal runes',
    'Distinctive jewelry',
    'Unique weapon/tool marks'
  ],
  clothing: [
    'Ornate robes with mystical symbols',
    'Well-worn but maintained armor',
    'Practical adventuring gear',
    'Exotic foreign garments',
    'Simple but elegant attire'
  ]
};

const colors = {
  eyes: ['azure', 'emerald', 'amber', 'violet', 'steel gray', 'deep brown', 'gold-flecked'],
  hair: ['raven black', 'golden', 'copper', 'silver', 'chestnut', 'platinum', 'midnight blue']
};

export interface AppearanceProfile {
  physicalDescription: string;
  distinguishingFeature: string;
  attire: string;
}

export function generateAppearance(race?: string, prompt?: string): AppearanceProfile {
  // If a prompt is provided, use it to influence appearance generation
  if (prompt) {
    // TODO: Implement more sophisticated prompt-based appearance generation
    return {
      physicalDescription: prompt,
      distinguishingFeature: 'Unique to their nature',
      attire: 'Suited to their character'
    };
  }

  const getRandomElement = (arr: string[]) => arr[Math.floor(Math.random() * arr.length)];

  // Generate base appearance
  const height = getRandomElement(physicalTraits.height);
  const build = getRandomElement(physicalTraits.build);
  const complexion = getRandomElement(physicalTraits.complexion);
  
  // Generate eyes and hair with random colors
  const eyeColor = getRandomElement(colors.eyes);
  const hairColor = getRandomElement(colors.hair);
  const eyes = getRandomElement(physicalTraits.eyes).replace('{color}', eyeColor);
  const hair = getRandomElement(physicalTraits.hair).replace('{color}', hairColor);

  // Combine into a coherent description
  const physicalDescription = `${height}, with a ${build} frame. ${complexion} skin complements their ${eyes}. ${hair}.`;

  return {
    physicalDescription,
    distinguishingFeature: getRandomElement(physicalTraits.distinguishingFeatures),
    attire: getRandomElement(physicalTraits.clothing)
  };
}
