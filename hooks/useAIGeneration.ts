import { useState } from 'react';
import { 
  generateDefaultPrompt, 
  validatePrompt, 
  enhancePrompt, 
  formatAIResponse,
  AIGenerationResponse 
} from '../utils/aiGenerationUtils';
import { ProfilePicturePromptHelper } from '../utils/promptHelpers';
import { generateProfilePicture } from '@/services/huggingFaceService';

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

      // TODO: Replace with actual API call to AI service
      const response = await mockAICall(enhancedPrompt);

      if (!response.success) {
        throw new Error(response.error || 'Failed to generate content');
      }

      const formattedContent = formatAIResponse(field!, response.content!);
      
      onSuccess?.(formattedContent);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(errorMessage);
      onError?.(errorMessage);
    } finally {
      setIsLoading(false);
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
      const imageBlob = await generateProfilePicture(enhancedPrompt);
      
      // Convert blob to File
      const file = new File([imageBlob], 'profile-picture.png', { type: 'image/png' });
      
      // Create form data
      const formData = new FormData();
      formData.append('image', file);

      // Upload the image to local storage
      const response = await fetch('/api/upload-image', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload generated image');
      }

      const { imageUrl } = await response.json();
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
