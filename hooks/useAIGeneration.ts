import { useState } from 'react';
import { 
  generateDefaultPrompt, 
  validatePrompt, 
  enhancePrompt, 
  formatAIResponse,
  AIGenerationResponse 
} from '../utils/aiGenerationUtils';
import { ProfilePicturePromptHelper } from '../utils/promptHelpers';

interface UseAIGenerationProps {
  field?: string;
  currentCharacter?: any;
  onSuccess?: (content: string) => void;
  onError?: (error: string) => void;
}

interface GenerateImageParams {
  prompt: string;
  qualityModifier?: string;
  negativePrompt?: string;
}

export const useAIGeneration = ({
  field,
  currentCharacter,
  onSuccess,
  onError
}: UseAIGenerationProps = {}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateContent = async (customPrompt?: string): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      // Use custom prompt if provided, otherwise generate default
      let prompt = customPrompt || generateDefaultPrompt(field!, currentCharacter);

      // Validate the prompt
      if (!validatePrompt(prompt)) {
        throw new Error('Invalid prompt. Please try again with different wording.');
      }

      // Enhance the prompt with guidelines
      const enhancedPrompt = enhancePrompt(field!, prompt);

      try {
        const response = await mockAICall(enhancedPrompt);
        if (!response.success) {
          throw new Error(response.error || 'Failed to generate content.');
        }
        const formattedContent = formatAIResponse(field!, response.content!);
        onSuccess?.(formattedContent);
      } catch (error) {
        console.error('Error during AI content generation:', error);
        setError(error.message);
        onError?.(error.message);
      } finally {
        setIsLoading(false);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(errorMessage);
      onError?.(errorMessage);
    }
  };

  const generateImage = async ({
    prompt,
    qualityModifier = 'high quality',
    negativePrompt = 'low quality, blurry, distorted',
  }: GenerateImageParams): Promise<string> => {
    setIsLoading(true);
    setError(null);

    try {
      const enhancedPrompt = `${prompt}, ${qualityModifier}, fantasy style, detailed, professional lighting`;

      // Call the new API route
      const response = await fetch('/api/generate-profile-picture', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: enhancedPrompt }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate image');
      }

      const data = await response.json();
      const imageUrl = data.image; // This should be a Base64 string

      onSuccess?.(imageUrl);
      return imageUrl;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to generate image');
      setError(error.message);
      onError?.(error.message);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  return {
    generateContent,
    generateImage,
    isLoading,
    error,
  };
};

// Mock function for development
const mockAICall = async (prompt: string): Promise<AIGenerationResponse> => {
  await new Promise(resolve => setTimeout(resolve, 1000));
  return {
    success: true,
    content: 'Mocked AI response for: ' + prompt,
  };
};

export default useAIGeneration;
