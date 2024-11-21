import { NextApiRequest, NextApiResponse } from 'next';
import formidable from 'formidable';
import { uploadImage } from '@/services/localStorageService';
import fs from 'fs';

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const form = new formidable.IncomingForm();
    form.parse(req, async (err, _fields, files) => {
      if (err) {
        return res.status(400).json({ error: 'Error parsing form data' });
      }

      const imageFile = files.image as formidable.File;
      if (!imageFile) {
        return res.status(400).json({ error: 'No image file provided' });
      }

      const fileContent = fs.readFileSync(imageFile.filepath);
      const imageUrl = await uploadImage(fileContent, imageFile.mimetype || 'image/png');

      return res.status(200).json({ imageUrl });
    });
  } catch (error) {
    console.error('Error uploading image:', error);
    return res.status(500).json({ error: 'Error uploading image' });
  }
}
