// Example interface for AI content generation
import { generateName } from './nameGenerator';
import { generateBackstory } from './backstoryGenerator';
import { generatePersonality, PersonalityProfile } from './personalityGenerator';
import { generateAppearance, AppearanceProfile } from './appearanceGenerator';
import { DndBackground, DndClass, DndRace } from './dnd5eData';

export interface AIContentGenerator {
  generateName(race?: DndRace, prompt?: string): string;
  generateBackstory(params: {
    name: string;
    race?: DndRace;
    class?: DndClass;
    background?: DndBackground;
    prompt?: string;
  }): string;
  generatePersonality(prompt?: string): PersonalityProfile;
  generateAppearance(race?: DndRace, prompt?: string): AppearanceProfile;
}

export class LocalContentGenerator implements AIContentGenerator {
  generateName(race?: DndRace, prompt?: string): string {
    return generateName(race, prompt);
  }

  generateBackstory(params: {
    name: string;
    race?: DndRace;
    class?: DndClass;
    background?: DndBackground;
    prompt?: string;
  }): string {
    return generateBackstory(params);
  }

  generatePersonality(prompt?: string): PersonalityProfile {
    return generatePersonality(prompt);
  }

  generateAppearance(race?: DndRace, prompt?: string): AppearanceProfile {
    return generateAppearance(race, prompt);
  }
}

// This will be replaced with actual AI implementation later
export class AIContentGeneratorImpl extends LocalContentGenerator {
  // Override methods with AI-powered implementations when ready
}

// Export an instance of the placeholder generator
export const aiGenerator: AIContentGenerator = new LocalContentGenerator();
