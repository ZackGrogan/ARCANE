export const fieldHelpText = {
  Name: "Generate a name that fits the character's race and background. You can specify cultural influences or naming conventions.",
  Race: "Generate a race from D&D 5e. You can specify preferences like 'common races only' or 'exotic races preferred'.",
  Class: "Generate a class from D&D 5e. You can specify combat style, magical ability, or roleplay preferences.",
  Backstory: "Generate a character backstory. Include details about origin, motivations, and significant life events.",
  PersonalityTraits: "Generate personality traits, ideals, bonds, and flaws that shape the character's behavior and decisions.",
  Appearance: "Generate a physical description including height, build, distinctive features, and clothing style."
};

export const examplePrompts = {
  Name: [
    "A noble elven name with a mystical feel",
    "A gruff dwarven name suitable for a blacksmith",
    "A human name from a coastal trading city"
  ],
  Race: [
    "A race well-suited for diplomatic missions",
    "A race with natural magical abilities",
    "A physically robust race for front-line combat"
  ],
  Class: [
    "A spellcaster who specializes in healing",
    "A stealthy character who excels at reconnaissance",
    "A warrior who protects their allies"
  ],
  Backstory: [
    "A character who grew up in a merchant family",
    "Someone who survived a tragic event in their hometown",
    "A scholar who discovered forbidden knowledge"
  ],
  PersonalityTraits: [
    "A charismatic leader with a dark secret",
    "A cautious strategist who values preparation",
    "An optimistic adventurer seeking glory"
  ],
  Appearance: [
    "A battle-scarred veteran with distinctive armor",
    "A mysterious figure in flowing robes",
    "A charming noble with elegant attire"
  ]
};

export const contentGuidelines = {
  Name: {
    dos: [
      "Use names that fit the race's culture",
      "Consider the character's background",
      "Keep names pronounceable"
    ],
    donts: [
      "Avoid offensive or inappropriate terms",
      "Don't use copyrighted names",
      "Avoid overly complex names"
    ]
  },
  Race: {
    dos: [
      "Stick to official D&D 5e races",
      "Consider racial traits and abilities",
      "Think about cultural implications"
    ],
    donts: [
      "Don't create unofficial races",
      "Avoid stereotypical descriptions",
      "Don't ignore racial limitations"
    ]
  },
  Class: {
    dos: [
      "Use official D&D 5e classes",
      "Consider multiclass possibilities",
      "Think about party role"
    ],
    donts: [
      "Don't create unofficial classes",
      "Avoid overpowered combinations",
      "Don't ignore class requirements"
    ]
  },
  Backstory: {
    dos: [
      "Create compelling motivations",
      "Include key life events",
      "Connect to the game world"
    ],
    donts: [
      "Avoid clichéd tropes",
      "Don't make them overpowered",
      "Avoid inappropriate content"
    ]
  },
  PersonalityTraits: {
    dos: [
      "Create balanced personalities",
      "Include flaws and weaknesses",
      "Consider alignment"
    ],
    donts: [
      "Avoid one-dimensional traits",
      "Don't make them perfect",
      "Avoid harmful stereotypes"
    ]
  },
  Appearance: {
    dos: [
      "Include distinctive features",
      "Consider race and class",
      "Add personal style"
    ],
    donts: [
      "Avoid inappropriate descriptions",
      "Don't ignore racial characteristics",
      "Avoid unrealistic features"
    ]
  }
};

export class ProfilePicturePromptHelper {
  static readonly EXAMPLE_PROMPTS = [
    'A battle-hardened dwarf warrior with a thick braided beard, wearing ornate plate armor and bearing scars from countless battles.',
    'An elegant high elf wizard with flowing silver hair, adorned in mystical robes with intricate arcane symbols.',
    'A mysterious tiefling rogue with deep purple skin, curved horns, and a mischievous smile, wearing dark leather armor.',
  ];

  static readonly QUALITY_GUIDELINES = {
    composition: [
      'Clear facial features and expressions',
      'Well-defined lighting and shadows',
      'Balanced composition and framing',
    ],
    style: [
      'Consistent with D&D 5e art style',
      'Professional fantasy portrait quality',
      'Appropriate level of detail',
    ],
    content: [
      'Character-appropriate clothing and accessories',
      'Race-specific features accurately represented',
      'Mood and atmosphere matching character background',
    ],
  };

  static readonly NEGATIVE_PROMPTS = [
    'low quality',
    'blurry',
    'distorted',
    'inappropriate content',
    'oversaturated',
    'poorly lit',
    'missing details',
  ];

  static getExamplePrompt(): string {
    return this.EXAMPLE_PROMPTS[Math.floor(Math.random() * this.EXAMPLE_PROMPTS.length)];
  }

  static getQualityGuideline(category: keyof typeof this.QUALITY_GUIDELINES): string[] {
    return this.QUALITY_GUIDELINES[category];
  }

  static getNegativePrompts(): string {
    return this.NEGATIVE_PROMPTS.join(', ');
  }

  static enhancePrompt(basePrompt: string, qualityModifier: string): string {
    return `${basePrompt}, ${qualityModifier}, fantasy character portrait, detailed features, professional lighting`;
  }
}
