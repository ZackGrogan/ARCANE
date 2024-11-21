import React from 'react';
import { FormControl, InputLabel, Select, MenuItem, SelectChangeEvent, Box, Tooltip, IconButton } from '@mui/material';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';

interface QualityModifierSelectProps {
  value: string;
  onChange: (value: string) => void;
}

const QUALITY_MODIFIERS = [
  {
    value: 'high quality',
    label: 'High Quality',
    description: 'Generate a high-quality image with detailed features and clear rendering.',
  },
  {
    value: 'masterpiece',
    label: 'Masterpiece',
    description: 'Generate an exceptional quality image with artistic flair and intricate details.',
  },
  {
    value: 'professional',
    label: 'Professional',
    description: 'Generate a professionally styled image with balanced composition and lighting.',
  },
  {
    value: 'realistic',
    label: 'Realistic',
    description: 'Generate a realistic image with natural features and textures.',
  },
];

export const QualityModifierSelect: React.FC<QualityModifierSelectProps> = ({ value, onChange }) => {
  const handleChange = (event: SelectChangeEvent) => {
    onChange(event.target.value);
  };

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
      <FormControl fullWidth>
        <InputLabel id="quality-modifier-label">Quality Style</InputLabel>
        <Select
          labelId="quality-modifier-label"
          value={value}
          label="Quality Style"
          onChange={handleChange}
        >
          {QUALITY_MODIFIERS.map((modifier) => (
            <MenuItem key={modifier.value} value={modifier.value}>
              {modifier.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <Tooltip title={QUALITY_MODIFIERS.find(m => m.value === value)?.description || ''}>
        <IconButton size="small">
          <HelpOutlineIcon />
        </IconButton>
      </Tooltip>
    </Box>
  );
};
