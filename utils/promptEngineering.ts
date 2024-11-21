interface PromptOptions {
  qualityModifiers?: string[];
  negativePrompts?: string[];
}

export const constructPrompt = (description: string, options: PromptOptions = {}): string => {
  let prompt = description;

  if (options.qualityModifiers) {
    prompt += ' ' + options.qualityModifiers.join(' ');
  }

  if (options.negativePrompts) {
    prompt += ' Avoid: ' + options.negativePrompts.join(', ');
  }

  return prompt;
};

export const defaultQualityModifiers = [
  'high resolution',
  'realistic',
  'detailed'
];

export const defaultNegativePrompts = [
  'blurry',
  'distorted',
  'unrealistic colors'
];
