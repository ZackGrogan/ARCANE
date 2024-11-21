import React, { useState } from 'react';
import {
  Box,
  Button,
  CircularProgress,
  TextField,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
  Card,
  CardContent,
  Alert,
  AlertTitle,
  LinearProgress,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import RefreshIcon from '@mui/icons-material/Refresh';
import SaveIcon from '@mui/icons-material/Save';
import { generateEncounter } from '@/services/encounterGenerationService';
import { ErrorBoundary } from 'react-error-boundary';

interface PartyInfo {
  size: number;
  averageLevel: number;
}

interface EncounterModifiers {
  environment?: string;
  theme?: string;
  constraints?: string[];
}

const environments = [
  'Arctic', 'Coastal', 'Desert', 'Forest', 'Grassland',
  'Mountain', 'Swamp', 'Underdark', 'Underwater', 'Urban'
];

const themes = [
  'Mystery', 'Horror', 'Action', 'Exploration',
  'Social', 'Stealth', 'Survival', 'Combat'
];

const ErrorFallback = ({ error, resetErrorBoundary }) => (
  <Box role="alert" p={3}>
    <Alert severity="error">
      <AlertTitle>Something went wrong</AlertTitle>
      <Typography>{error.message}</Typography>
      <Button 
        onClick={resetErrorBoundary}
        variant="contained" 
        sx={{ mt: 2 }}
      >
        Try again
      </Button>
    </Alert>
  </Box>
);

const EncounterGenerator: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [encounter, setEncounter] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  // Advanced options state
  const [partyInfo, setPartyInfo] = useState<PartyInfo>({
    size: 4,
    averageLevel: 1,
  });
  const [modifiers, setModifiers] = useState<EncounterModifiers>({
    environment: '',
    theme: '',
    constraints: [],
  });

  const handleGenerate = async (quickGenerate: boolean = false) => {
    if (!prompt.trim()) {
      setError('Please enter a prompt for the encounter');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const options = {
        partyInfo,
        modifiers: quickGenerate ? undefined : modifiers,
        quickGenerate,
      };
      const generatedEncounter = await generateEncounter(prompt, options);
      setEncounter(generatedEncounter);
    } catch (err) {
      setError('Failed to generate encounter. Please try again.');
      console.error('Encounter generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRegenerateSection = async (section: string) => {
    setLoading(true);
    setError(null);
    try {
      // Implement section regeneration
      console.log(`Regenerating section: ${section}`);
    } catch (err) {
      setError(`Failed to regenerate ${section}. Please try again.`);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveEncounter = async () => {
    if (!encounter) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/encounters', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(encounter),
      });
      
      if (!response.ok) {
        throw new Error('Failed to save encounter');
      }
      
      // Show success message
      console.log('Encounter saved successfully');
    } catch (err) {
      setError('Failed to save encounter. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onReset={() => {
        setError(null);
        setLoading(false);
        setEncounter(null);
      }}
    >
      <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }} role="main" aria-label="Encounter Generator">
        <Typography variant="h4" gutterBottom>
          Random Encounter Generator
        </Typography>
        
        {loading && <LinearProgress sx={{ mb: 2 }} />}
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }} role="alert">
            <AlertTitle>Error</AlertTitle>
            {error}
          </Alert>
        )}
        
        {/* Quick Generate Section */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <TextField
              fullWidth
              multiline
              rows={3}
              label="Encounter Prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the encounter you'd like to generate"
              sx={{ mb: 2 }}
              disabled={loading}
              error={!prompt.trim() && error !== null}
              helperText={!prompt.trim() && error !== null ? 'Please enter a prompt' : ''}
              aria-label="Enter encounter prompt"
              required
            />
            <Button
              variant="contained"
              onClick={() => handleGenerate(true)}
              disabled={!prompt.trim() || loading}
              startIcon={loading ? <CircularProgress size={20} /> : null}
              fullWidth
              aria-busy={loading}
            >
              {loading ? 'Generating...' : 'Quick Generate'}
            </Button>
          </CardContent>
        </Card>

        {/* Advanced Options */}
        <Accordion 
          expanded={showAdvanced} 
          onChange={() => setShowAdvanced(!showAdvanced)}
          disabled={loading}
        >
          <AccordionSummary 
            expandIcon={<ExpandMoreIcon />}
            aria-controls="advanced-options-content"
            id="advanced-options-header"
          >
            <Typography>Advanced Options</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel id="party-size-label">Party Size</InputLabel>
                  <Select
                    labelId="party-size-label"
                    value={partyInfo.size}
                    onChange={(e) => setPartyInfo({ ...partyInfo, size: Number(e.target.value) })}
                    disabled={loading}
                  >
                    {[1, 2, 3, 4, 5, 6, 7, 8].map((size) => (
                      <MenuItem key={size} value={size}>{size} Players</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel id="level-label">Average Level</InputLabel>
                  <Select
                    labelId="level-label"
                    value={partyInfo.averageLevel}
                    onChange={(e) => setPartyInfo({ ...partyInfo, averageLevel: Number(e.target.value) })}
                    disabled={loading}
                  >
                    {Array.from({ length: 20 }, (_, i) => i + 1).map((level) => (
                      <MenuItem key={level} value={level}>Level {level}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel id="environment-label">Environment</InputLabel>
                  <Select
                    labelId="environment-label"
                    value={modifiers.environment}
                    onChange={(e) => setModifiers({ ...modifiers, environment: e.target.value })}
                    disabled={loading}
                  >
                    <MenuItem value="">Any</MenuItem>
                    {environments.map((env) => (
                      <MenuItem key={env} value={env}>{env}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} sm={6}>
                <FormControl fullWidth>
                  <InputLabel id="theme-label">Theme</InputLabel>
                  <Select
                    labelId="theme-label"
                    value={modifiers.theme}
                    onChange={(e) => setModifiers({ ...modifiers, theme: e.target.value })}
                    disabled={loading}
                  >
                    <MenuItem value="">Any</MenuItem>
                    {themes.map((theme) => (
                      <MenuItem key={theme} value={theme}>{theme}</MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
            <Button
              variant="contained"
              onClick={() => handleGenerate(false)}
              disabled={!prompt.trim() || loading}
              sx={{ mt: 2 }}
              startIcon={loading ? <CircularProgress size={20} /> : null}
              fullWidth
            >
              {loading ? 'Generating...' : 'Generate with Options'}
            </Button>
          </AccordionDetails>
        </Accordion>

        {/* Generated Encounter Display */}
        {encounter && (
          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h5">{encounter.title}</Typography>
                <Box>
                  <IconButton
                    onClick={() => handleRegenerateSection('all')}
                    disabled={loading}
                    aria-label="Regenerate encounter"
                  >
                    <RefreshIcon />
                  </IconButton>
                  <IconButton
                    onClick={handleSaveEncounter}
                    disabled={loading}
                    aria-label="Save encounter"
                  >
                    <SaveIcon />
                  </IconButton>
                </Box>
              </Box>
              <Typography variant="body1" paragraph>
                {encounter.description}
              </Typography>
              {/* Add more encounter details here */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Environment
                  <Tooltip title="Regenerate Environment">
                    <IconButton size="small" onClick={() => handleRegenerateSection('environment')}>
                      <RefreshIcon />
                    </IconButton>
                  </Tooltip>
                </Typography>
                <Grid container spacing={1}>
                  <Grid item><Chip label={`Biome: ${encounter.biome}`} /></Grid>
                  <Grid item><Chip label={`Weather: ${encounter.weather}`} /></Grid>
                  {encounter.environmentDetails.specialFeatures.map((feature: string, index: number) => (
                    <Grid item key={index}><Chip label={feature} /></Grid>
                  ))}
                </Grid>
              </Box>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Monsters
                  <Tooltip title="Regenerate Monsters">
                    <IconButton size="small" onClick={() => handleRegenerateSection('monsters')}>
                      <RefreshIcon />
                    </IconButton>
                  </Tooltip>
                </Typography>
                <Grid container spacing={2}>
                  {encounter.monsters.map((monster: any, index: number) => (
                    <Grid item xs={12} sm={6} key={index}>
                      <Card variant="outlined">
                        <CardContent>
                          <Typography variant="subtitle1">{monster.name}</Typography>
                          <Typography variant="body2">Quantity: {monster.quantity}</Typography>
                          {monster.stats && (
                            <Typography variant="body2">
                              CR: {monster.stats.challenge_rating} (XP: {monster.stats.xp})
                            </Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </Box>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Tactics
                  <Tooltip title="Regenerate Tactics">
                    <IconButton size="small" onClick={() => handleRegenerateSection('tactics')}>
                      <RefreshIcon />
                    </IconButton>
                  </Tooltip>
                </Typography>
                <ul>
                  {encounter.tactics.map((tactic: string, index: number) => (
                    <li key={index}><Typography variant="body1">{tactic}</Typography></li>
                  ))}
                </ul>
              </Box>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Loot
                  <Tooltip title="Regenerate Loot">
                    <IconButton size="small" onClick={() => handleRegenerateSection('loot')}>
                      <RefreshIcon />
                    </IconButton>
                  </Tooltip>
                </Typography>
                <Grid container spacing={1}>
                  {encounter.loot.map((item: any, index: number) => (
                    <Grid item xs={12} sm={6} md={4} key={index}>
                      <Chip
                        label={`${item.quantity}x ${item.item} (${item.rarity})`}
                        sx={{ width: '100%' }}
                      />
                    </Grid>
                  ))}
                </Grid>
              </Box>
              <Box>
                <Typography variant="h6" gutterBottom>
                  Roleplaying Opportunities
                  <Tooltip title="Regenerate Scenarios">
                    <IconButton size="small" onClick={() => handleRegenerateSection('roleplayingScenarios')}>
                      <RefreshIcon />
                    </IconButton>
                  </Tooltip>
                </Typography>
                <ul>
                  {encounter.roleplayingScenarios.map((scenario: string, index: number) => (
                    <li key={index}><Typography variant="body1">{scenario}</Typography></li>
                  ))}
                </ul>
              </Box>
            </CardContent>
          </Card>
        )}
      </Box>
    </ErrorBoundary>
  );
};

export default EncounterGenerator;
