import { useState } from 'react';
import { 
  generateDefaultPrompt, 
  validatePrompt, 
  enhancePrompt, 
  formatAIResponse,
  AIGenerationResponse 
} from '../utils/aiGenerationUtils';

interface UseAIGenerationProps {
  field: string;
  currentCharacter?: any;
  onSuccess?: (content: string) => void;
  onError?: (error: string) => void;
}

export const useAIGeneration = ({
  field,
  currentCharacter,
  onSuccess,
  onError
}: UseAIGenerationProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generateContent = async (customPrompt?: string): Promise<void> => {
    setIsLoading(true);
    setError(null);

    try {
      // Use custom prompt if provided, otherwise generate default
      let prompt = customPrompt || generateDefaultPrompt(field, currentCharacter);

      // Validate the prompt
      if (!validatePrompt(prompt)) {
        throw new Error('Invalid prompt. Please try again with different wording.');
      }

      // Enhance the prompt with guidelines
      const enhancedPrompt = enhancePrompt(field, prompt);

      // TODO: Replace with actual API call to AI service
      const response = await mockAICall(enhancedPrompt);

      if (!response.success) {
        throw new Error(response.error || 'Failed to generate content');
      }

      const formattedContent = formatAIResponse(field, response.content!);
      
      onSuccess?.(formattedContent);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(errorMessage);
      onError?.(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // Mock AI call - replace with actual API implementation
  const mockAICall = async (prompt: string): Promise<AIGenerationResponse> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Simulate success response
    return {
      success: true,
      content: "Sample AI-generated content for " + field
    };
  };

  return {
    generateContent,
    isLoading,
    error
  };
};

export default useAIGeneration;
