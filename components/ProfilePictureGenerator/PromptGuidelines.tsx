import React from 'react';
import { Box, Paper, Typography, List, ListItem, ListItemIcon, ListItemText, Collapse } from '@mui/material';
import TipsAndUpdatesIcon from '@mui/icons-material/TipsAndUpdates';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

const PROMPT_TIPS = [
  {
    text: 'Be specific about facial features, expressions, and clothing',
    icon: <CheckCircleOutlineIcon color="success" />,
  },
  {
    text: 'Include details about race, age, and distinguishing characteristics',
    icon: <CheckCircleOutlineIcon color="success" />,
  },
  {
    text: 'Mention the mood or atmosphere you want to convey',
    icon: <CheckCircleOutlineIcon color="success" />,
  },
];

const CONTENT_GUIDELINES = [
  {
    text: 'Avoid explicit or inappropriate content',
    icon: <ErrorOutlineIcon color="error" />,
  },
  {
    text: 'Keep descriptions aligned with D&D 5e themes and settings',
    icon: <CheckCircleOutlineIcon color="success" />,
  },
  {
    text: 'Focus on character-defining features rather than generic descriptions',
    icon: <CheckCircleOutlineIcon color="success" />,
  },
];

export const PromptGuidelines: React.FC = () => {
  const [expanded, setExpanded] = React.useState(true);

  return (
    <Paper elevation={0} sx={{ p: 2, mb: 3, bgcolor: 'background.default' }}>
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          gap: 1,
          cursor: 'pointer',
        }}
        onClick={() => setExpanded(!expanded)}
      >
        <TipsAndUpdatesIcon color="primary" />
        <Typography variant="subtitle1" color="primary">
          Writing Effective Descriptions
        </Typography>
      </Box>

      <Collapse in={expanded}>
        <Box sx={{ mt: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            Tips for Better Results:
          </Typography>
          <List dense>
            {PROMPT_TIPS.map((tip, index) => (
              <ListItem key={index}>
                <ListItemIcon sx={{ minWidth: 36 }}>{tip.icon}</ListItemIcon>
                <ListItemText primary={tip.text} />
              </ListItem>
            ))}
          </List>

          <Typography variant="subtitle2" gutterBottom sx={{ mt: 2 }}>
            Content Guidelines:
          </Typography>
          <List dense>
            {CONTENT_GUIDELINES.map((guideline, index) => (
              <ListItem key={index}>
                <ListItemIcon sx={{ minWidth: 36 }}>{guideline.icon}</ListItemIcon>
                <ListItemText primary={guideline.text} />
              </ListItem>
            ))}
          </List>
        </Box>
      </Collapse>
    </Paper>
  );
};
