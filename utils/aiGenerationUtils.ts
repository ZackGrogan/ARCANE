import { fieldHelpText, examplePrompts, contentGuidelines } from './promptHelpers';

export interface AIGenerationResponse {
  success: boolean;
  content?: string;
  error?: string;
}

export const generateDefaultPrompt = (field: string, currentCharacter: any): string => {
  const basePrompts = {
    Name: "Generate a fantasy name suitable for a D&D character",
    Race: "Generate a D&D 5e race",
    Class: "Generate a D&D 5e class",
    Backstory: "Generate a compelling backstory for a D&D character",
    PersonalityTraits: "Generate personality traits for a D&D character",
    Appearance: "Generate a physical description for a D&D character"
  };

  let prompt = basePrompts[field as keyof typeof basePrompts] || "";

  // Enhance prompt based on existing character information
  if (currentCharacter) {
    if (!currentCharacter) return prompt;
    if (currentCharacter.race && field !== 'Race') {
      prompt += ` of ${currentCharacter.race} race`;
    }
    if (currentCharacter.class && field !== 'Class') {
      prompt += ` with ${currentCharacter.class} class`;
    }
  }

  return prompt;
};

export const validatePrompt = (prompt: string): boolean => {
  // Basic validation rules
  if (!prompt || prompt.trim().length === 0) return false;
  if (prompt.length > 500) return false; // Reasonable length limit
  
  // Check for inappropriate content (basic check)
  const inappropriateTerms = [
    "offensive",
    "inappropriate",
    "explicit",
    "violent",
    "racist",
    "sexist",
    // Add more terms as needed
  ];
  
  return !inappropriateTerms.some(term => 
    prompt.toLowerCase().includes(term)
  );
};

export const enhancePrompt = (field: string, basePrompt: string): string => {
  const guidelines = contentGuidelines[field as keyof typeof contentGuidelines];
  let enhancedPrompt = basePrompt;

  // Add relevant guidelines to the prompt
  if (guidelines) {
    enhancedPrompt += "\nPlease follow these guidelines:";
    guidelines.dos.forEach(rule => {
      enhancedPrompt += `\n- Do: ${rule}`;
    });
    guidelines.donts.forEach(rule => {
      enhancedPrompt += `\n- Don't: ${rule}`;
    });
  }

  return enhancedPrompt;
};

export const formatAIResponse = (field: string, response: string): string => {
  // Remove any special characters or formatting that might have been added by the AI
  let formattedResponse = response.trim();

  // Field-specific formatting
  switch (field) {
    case 'Name':
      // Capitalize each word in the name
      formattedResponse = formattedResponse
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
      break;
    
    case 'Race':
    case 'Class':
      // Capitalize first letter only
      formattedResponse = formattedResponse.charAt(0).toUpperCase() + 
        formattedResponse.slice(1).toLowerCase();
      break;
    
    case 'Backstory':
    case 'PersonalityTraits':
    case 'Appearance':
      // Ensure proper sentence formatting
      formattedResponse = formattedResponse
        .split('. ')
        .map(sentence => sentence.charAt(0).toUpperCase() + sentence.slice(1))
        .join('. ');
      if (!formattedResponse.endsWith('.')) {
        formattedResponse += '.';
      }
      break;
  }

  return formattedResponse;
};

export const getFieldHelp = (field: string): string => {
  return fieldHelpText[field as keyof typeof fieldHelpText] || '';
};

export const getExamplePrompts = (field: string): string[] => {
  return examplePrompts[field as keyof typeof examplePrompts] || [];
};
