import { NextApiRequest, NextApiResponse } from 'next';
import { HuggingFaceService } from '@/services/huggingFaceService';
import { ImageStorageService } from '@/services/imageStorageService';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { prompt, negativePrompt } = req.body;

    if (!prompt) {
      return res.status(400).json({ error: 'Prompt is required' });
    }

    // Generate image using Hugging Face API
    const imageBuffer = await HuggingFaceService.generateImage({
      prompt,
      negativePrompt,
      model: 'stabilityai/stable-diffusion-2-1', // or your preferred model
    });

    // Upload the generated image to storage
    const imageUrl = await ImageStorageService.uploadImage(
      imageBuffer,
      'image/png',
      `generated-images/${Date.now()}-${Math.random().toString(36).substring(7)}.png`
    );

    return res.status(200).json({ imageUrl });
  } catch (error) {
    console.error('Error generating image:', error);
    return res.status(500).json({
      error: 'Failed to generate image',
      details: error instanceof Error ? error.message : 'Unknown error',
    });
  }
}
