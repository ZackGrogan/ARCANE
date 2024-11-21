import type { NextApiRequest, NextApiResponse } from 'next';
import { generateProfilePicture } from '@/services/huggingFaceService';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { prompt } = req.body;
  if (!prompt) {
    return res.status(400).json({ error: 'Prompt is required' });
  }

  try {
    const imageBlob = await generateProfilePicture(prompt);
    const base64 = await new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(imageBlob);
      reader.onloadend = () => {
        if (typeof reader.result === 'string') {
          resolve(reader.result);
        } else {
          reject('Failed to convert image to Base64.');
        }
      };
      reader.onerror = () => reject('Error reading blob data.');
    });

    return res.status(200).json({ image: base64 });
  } catch (error: any) {
    console.error('Error generating profile picture:', error);
    return res.status(500).json({ error: 'Failed to generate profile picture' });
  }
}
