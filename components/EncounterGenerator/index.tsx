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
  Slider,
  Grid,
  Card,
  CardContent,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import RefreshIcon from '@mui/icons-material/Refresh';
import SaveIcon from '@mui/icons-material/Save';
import { generateEncounter } from '@/services/encounterGenerationService';

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
    } finally {
      setLoading(false);
    }
  };

  const handleRegenerateSection = async (section: string) => {
    // TODO: Implement section regeneration
    console.log(`Regenerating section: ${section}`);
  };

  const handleSaveEncounter = async () => {
    // TODO: Implement encounter saving
    console.log('Saving encounter');
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Random Encounter Generator
      </Typography>
      
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
          />
          <Button
            variant="contained"
            onClick={() => handleGenerate(true)}
            disabled={!prompt.trim() || loading}
            startIcon={loading ? <CircularProgress size={20} /> : null}
            fullWidth
          >
            {loading ? 'Generating...' : 'Quick Generate'}
          </Button>
        </CardContent>
      </Card>

      {/* Advanced Options */}
      <Accordion expanded={showAdvanced} onChange={() => setShowAdvanced(!showAdvanced)}>
        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
          <Typography>Advanced Options</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Party Size</InputLabel>
                <Select
                  value={partyInfo.size}
                  onChange={(e) => setPartyInfo({ ...partyInfo, size: Number(e.target.value) })}
                >
                  {[1, 2, 3, 4, 5, 6, 7, 8].map((size) => (
                    <MenuItem key={size} value={size}>{size} Players</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Average Level</InputLabel>
                <Select
                  value={partyInfo.averageLevel}
                  onChange={(e) => setPartyInfo({ ...partyInfo, averageLevel: Number(e.target.value) })}
                >
                  {Array.from({ length: 20 }, (_, i) => i + 1).map((level) => (
                    <MenuItem key={level} value={level}>Level {level}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Environment</InputLabel>
                <Select
                  value={modifiers.environment}
                  onChange={(e) => setModifiers({ ...modifiers, environment: e.target.value })}
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
                <InputLabel>Theme</InputLabel>
                <Select
                  value={modifiers.theme}
                  onChange={(e) => setModifiers({ ...modifiers, theme: e.target.value })}
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
            startIcon={loading ? <CircularProgress size={20} /> : null}
            sx={{ mt: 3 }}
            fullWidth
          >
            Generate with Options
          </Button>
        </AccordionDetails>
      </Accordion>

      {error && <Typography color="error" sx={{ mt: 2 }}>{error}</Typography>}

      {/* Encounter Display */}
      {encounter && (
        <Card sx={{ mt: 4 }}>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h5">{encounter.title}</Typography>
              <Box>
                <Tooltip title="Save Encounter">
                  <IconButton onClick={handleSaveEncounter}>
                    <SaveIcon />
                  </IconButton>
                </Tooltip>
              </Box>
            </Box>

            {/* Description */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Description
                <Tooltip title="Regenerate Description">
                  <IconButton size="small" onClick={() => handleRegenerateSection('description')}>
                    <RefreshIcon />
                  </IconButton>
                </Tooltip>
              </Typography>
              <Typography variant="body1">{encounter.description}</Typography>
            </Box>

            {/* Environment */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>Environment</Typography>
              <Grid container spacing={1}>
                <Grid item><Chip label={`Biome: ${encounter.biome}`} /></Grid>
                <Grid item><Chip label={`Weather: ${encounter.weather}`} /></Grid>
                {encounter.environmentDetails.specialFeatures.map((feature: string, index: number) => (
                  <Grid item key={index}><Chip label={feature} /></Grid>
                ))}
              </Grid>
            </Box>

            {/* Monsters */}
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

            {/* Tactics */}
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

            {/* Loot */}
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

            {/* Roleplaying Scenarios */}
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
  );
};

export default EncounterGenerator;
