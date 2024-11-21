import React, { useState, useCallback } from 'react';
import { Box, Button, TextField, Typography, CircularProgress, Tooltip } from '@mui/material';
import Image from 'next/image';
import { useAIGeneration } from '@/hooks/useAIGeneration';
import { ProfilePicturePromptHelper } from '@/utils/promptHelpers';
import { QualityModifierSelect } from './QualityModifierSelect';
import { ImagePreview } from './ImagePreview';
import { PromptGuidelines } from './PromptGuidelines';

interface ProfilePictureGeneratorProps {
  initialDescription?: string;
  onImageGenerated: (imageUrl: string) => void;
  onError?: (error: Error) => void;
}

export const ProfilePictureGenerator: React.FC<ProfilePictureGeneratorProps> = ({
  initialDescription = '',
  onImageGenerated,
  onError,
}) => {
  const [description, setDescription] = useState(initialDescription);
  const [qualityModifier, setQualityModifier] = useState('high quality');
  const { generateImage, isLoading, error } = useAIGeneration();

  const handleGenerate = useCallback(async () => {
    try {
      const imageUrl = await generateImage({
        prompt: description,
        qualityModifier,
        negativePrompt: 'low quality, blurry, distorted, inappropriate content',
      });
      onImageGenerated(imageUrl);
    } catch (err) {
      console.error('Error generating image:', err);
      onError?.(err as Error);
    }
  }, [description, qualityModifier, generateImage, onImageGenerated, onError]);

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Generate Profile Picture
      </Typography>
      
      <PromptGuidelines />

      <TextField
        fullWidth
        multiline
        rows={4}
        label="Character Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder={ProfilePicturePromptHelper.getExamplePrompt()}
        helperText="Describe your character's appearance, including notable features, expressions, and style."
        sx={{ mb: 2 }}
      />

      <QualityModifierSelect
        value={qualityModifier}
        onChange={(value) => setQualityModifier(value)}
      />

      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <Button
          variant="contained"
          onClick={handleGenerate}
          disabled={!description.trim() || isLoading}
          startIcon={isLoading ? <CircularProgress size={20} /> : null}
        >
          {isLoading ? 'Generating...' : 'Generate Image'}
        </Button>

        <Tooltip title="Upload your own image instead">
          <Button variant="outlined" aria-label="Upload Image">
            Upload Image
          </Button>
        </Tooltip>
      </Box>

      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error.message}
        </Typography>
      )}

      <ImagePreview />
    </Box>
  );
};
