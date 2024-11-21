import { DndBackground, DndClass, DndRace } from './dnd5eData';

interface BackstoryTemplate {
  intro: string[];
  childhood: string[];
  motivation: string[];
  conflict: string[];
  resolution: string[];
}

const backstoryTemplates: BackstoryTemplate = {
  intro: [
    "Born into a {background} family in {location},",
    "Raised among the {race} communities of {location},",
    "Found as an orphan in the streets of {location},",
    "Brought up in a {background} guild in {location},"
  ],
  childhood: [
    "{name} showed early signs of {trait}.",
    "{name} spent their youth learning the ways of {background}.",
    "{name} was mentored by a renowned {class}.",
    "{name} discovered their affinity for {class_feature} at a young age."
  ],
  motivation: [
    "Driven by an insatiable desire for {goal},",
    "Seeking to prove themselves worthy of {goal},",
    "Haunted by {past_event}, they seek {goal},",
    "Inspired by {inspiration}, they pursue {goal}"
  ],
  conflict: [
    "but faced opposition from {antagonist}.",
    "yet {obstacle} stood in their way.",
    "though {challenge} tested their resolve.",
    "despite the warnings of {mentor}."
  ],
  resolution: [
    "Now, they travel the realms, determined to {quest}.",
    "Today, they continue their journey, hoping to {quest}.",
    "Their path now leads them to {quest}.",
    "The road ahead promises {quest}."
  ]
};

export function generateBackstory(params: {
  name: string;
  race?: DndRace;
  class?: DndClass;
  background?: DndBackground;
  prompt?: string;
}): string {
  const { name, race, background, prompt } = params;

  // If a prompt is provided, use it as a base for generation
  if (prompt) {
    // TODO: Implement more sophisticated prompt-based backstory generation
    return prompt;
  }

  // Select random elements from each template category
  const getRandomElement = (arr: string[]) => arr[Math.floor(Math.random() * arr.length)];
  
  let backstory = getRandomElement(backstoryTemplates.intro)
    + " " + getRandomElement(backstoryTemplates.childhood)
    + " " + getRandomElement(backstoryTemplates.motivation)
    + " " + getRandomElement(backstoryTemplates.conflict)
    + " " + getRandomElement(backstoryTemplates.resolution);

  // Replace placeholders with actual values
  backstory = backstory
    .replace(/{name}/g, name)
    .replace(/{race}/g, race || 'local')
    .replace(/{background}/g, background || 'humble')
    .replace(/{location}/g, 'a distant realm')
    .replace(/{trait}/g, 'exceptional potential')
    .replace(/{class_feature}/g, 'the arcane arts')
    .replace(/{goal}/g, 'greatness')
    .replace(/{past_event}/g, 'a mysterious prophecy')
    .replace(/{inspiration}/g, 'ancient legends')
    .replace(/{antagonist}/g, 'powerful rivals')
    .replace(/{obstacle}/g, 'countless challenges')
    .replace(/{challenge}/g, 'adversity')
    .replace(/{mentor}/g, 'their elders')
    .replace(/{quest}/g, 'fulfill their destiny');

  return backstory;
}
