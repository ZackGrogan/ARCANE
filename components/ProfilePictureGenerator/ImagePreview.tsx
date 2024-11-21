import React from 'react';
import { Box, Paper, Typography, IconButton, Tooltip, CircularProgress } from '@mui/material';
import Image from 'next/image';
import RefreshIcon from '@mui/icons-material/Refresh';
import DownloadIcon from '@mui/icons-material/Download';
import DeleteIcon from '@mui/icons-material/Delete';

interface ImagePreviewProps {
  imageUrl?: string;
  onRegenerate?: () => void;
  onDownload?: () => void;
  onDelete?: () => void;
}

export const ImagePreview: React.FC<ImagePreviewProps> = ({
  imageUrl,
  onRegenerate,
  onDownload,
  onDelete,
}) => {
  if (!imageUrl) {
    return null;
  }

  return (
    <Paper
      elevation={1}
      sx={{
        p: 2,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 2,
      }}
    >
      <Typography variant="subtitle2" color="text.secondary">
        Generated Image Preview
      </Typography>

      <Box
        sx={{
          position: 'relative',
          width: '100%',
          maxWidth: 400,
          aspectRatio: '1',
          borderRadius: 1,
          overflow: 'hidden',
        }}
      >
        {!imageUrl && <CircularProgress />}
        <Image
          src={imageUrl}
          alt="Generated profile picture"
          layout="fill"
          objectFit="cover"
        />
      </Box>

      <Box sx={{ display: 'flex', gap: 1 }}>
        {onRegenerate && (
          <Tooltip title="Generate a new image with the same description">
            <IconButton onClick={onRegenerate} size="small">
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        )}

        {onDownload && (
          <Tooltip title="Download image">
            <IconButton onClick={onDownload} size="small">
              <DownloadIcon />
            </IconButton>
          </Tooltip>
        )}

        {onDelete && (
          <Tooltip title="Delete image">
            <IconButton onClick={onDelete} size="small" color="error">
              <DeleteIcon />
            </IconButton>
          </Tooltip>
        )}
      </Box>
    </Paper>
  );
};
