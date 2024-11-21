import React, { useState } from 'react';
import axios from 'axios';
import { aiGenerator } from '../services/aiService';
import { useForm } from 'react-hook-form';
import AIGenerationModal from './AIGenerationModal';
import { ProfilePictureGenerator } from './ProfilePictureGenerator';
import { useAIGeneration } from '../hooks/useAIGeneration';
import { Box, Button, Grid, TextField, Typography, Paper } from '@mui/material';

interface NPCFormData {
  name: string;
  race: string;
  class: string;
  backstory: string;
  personalityTraits: string;
  appearance: string;
  background: string;
  alignment: string;
  skills: string;
  equipment: string;
  profilePicture?: string;
}

const NPCForm = () => {
  const { register, handleSubmit, setValue, watch } = useForm<NPCFormData>();
  const [selectedField, setSelectedField] = useState<keyof NPCFormData | null>(null);
  const [showProfilePictureGenerator, setShowProfilePictureGenerator] = useState(false);
  const currentValues = watch();
  const { generateImage, isLoading: imageLoading } = useAIGeneration({});

  const handleAIGenerate = (field: keyof NPCFormData) => {
    setSelectedField(field);
  };

  const handleGeneratedContent = (content: string) => {
    if (selectedField) {
      setValue(selectedField, content);
    }
    setSelectedField(null);
  };

  const handleProfilePictureGenerated = (imageUrl: string) => {
    setValue('profilePicture', imageUrl);
    setShowProfilePictureGenerator(false);
  };

  const handleSubmitForm = async (data: NPCFormData) => {
    try {
      const response = await axios.post('/api/npcs', data);
      // Handle successful submission
      console.log('NPC created:', response.data);
    } catch (error) {
      // Handle error
      console.error('Error creating NPC:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(handleSubmitForm)}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          {/* Basic Information */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Basic Information
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Name"
                  {...register('name', { required: true })}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Race"
                  {...register('race', { required: true })}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Class"
                  {...register('class', { required: true })}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Background"
                  {...register('background', { required: true })}
                />
              </Grid>
            </Grid>
          </Paper>

          {/* Character Details */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Character Details
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  label="Appearance"
                  {...register('appearance')}
                  InputProps={{
                    endAdornment: (
                      <Button
                        onClick={() => handleAIGenerate('appearance')}
                        disabled={imageLoading}
                      >
                        Generate
                      </Button>
                    ),
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  label="Personality Traits"
                  {...register('personalityTraits')}
                  InputProps={{
                    endAdornment: (
                      <Button onClick={() => handleAIGenerate('personalityTraits')}>
                        Generate
                      </Button>
                    ),
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  label="Backstory"
                  {...register('backstory')}
                  InputProps={{
                    endAdornment: (
                      <Button onClick={() => handleAIGenerate('backstory')}>
                        Generate
                      </Button>
                    ),
                  }}
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Profile Picture Section */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Profile Picture
            </Typography>
            {currentValues.profilePicture ? (
              <Box
                sx={{
                  position: 'relative',
                  width: '100%',
                  paddingTop: '100%',
                  mb: 2,
                }}
              >
                <Box
                  component="img"
                  src={currentValues.profilePicture}
                  alt="Character profile"
                  sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    borderRadius: 1,
                  }}
                />
              </Box>
            ) : (
              <Box
                sx={{
                  width: '100%',
                  paddingTop: '100%',
                  bgcolor: 'grey.100',
                  borderRadius: 1,
                  mb: 2,
                }}
              />
            )}
            <Button
              fullWidth
              variant="contained"
              onClick={() => setShowProfilePictureGenerator(true)}
              disabled={imageLoading}
            >
              {currentValues.profilePicture ? 'Change Picture' : 'Generate Picture'}
            </Button>
          </Paper>
        </Grid>
      </Grid>

      {/* Submit Button */}
      <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          size="large"
        >
          Create NPC
        </Button>
      </Box>

      {/* AI Generation Modal */}
      {selectedField && (
        <AIGenerationModal
          open={!!selectedField}
          onClose={() => setSelectedField(null)}
          onGenerated={handleGeneratedContent}
          field={selectedField}
          currentCharacter={currentValues}
        />
      )}

      {/* Profile Picture Generator Modal */}
      {showProfilePictureGenerator && (
        <ProfilePictureGenerator
          initialDescription={currentValues.appearance}
          onImageGenerated={handleProfilePictureGenerated}
          onError={(error) => console.error('Error generating profile picture:', error)}
        />
      )}
    </form>
  );
};

export default NPCForm;
