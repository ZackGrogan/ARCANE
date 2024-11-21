import { NextApiRequest, NextApiResponse } from 'next';
import { dbConnect } from '@/lib/dbConnect';
import { NPC } from '@/models/npc';
import { isValidObjectId } from 'mongoose';
import formidable from 'formidable';
import fs from 'fs';
import { uploadImage, deleteImage } from '@/services/localStorageService';

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { method } = req;
  const { id } = req.query;

  if (!id || typeof id !== 'string') {
    return res.status(400).json({ error: 'Invalid NPC ID' });
  }

  if (!isValidObjectId(id)) {
    return res.status(400).json({ error: 'Invalid NPC ID format' });
  }

  try {
    await dbConnect();

    switch (method) {
      case 'GET': {
        const npc = await NPC.findById(id).lean();
        
        if (!npc) {
          return res.status(404).json({ error: 'NPC not found' });
        }

        return res.status(200).json(npc);
      }

      case 'PATCH': {
        const form = new formidable.IncomingForm();

        form.parse(req, async (err, fields, files) => {
          if (err) {
            return res.status(400).json({ error: 'Error parsing form data' });
          }

          const updateData = fields;
          const npc = await NPC.findById(id);
          if (!npc) {
            return res.status(404).json({ error: 'NPC not found' });
          }

          if (files.profileImage) {
            const file = files.profileImage as formidable.File;
            const fileContent = fs.readFileSync(file.filepath);

            if (npc.profileImage) {
              const oldFileName = npc.profileImage.split('/').pop();
              if (oldFileName) {
                await deleteImage(oldFileName);
              }
            }

            const imageUrl = await uploadImage(fileContent, file.mimetype);
            updateData.profileImage = imageUrl;
          }

          Object.assign(npc, updateData);
          await npc.save();

          return res.status(200).json(npc);
        });
        break;
      }

      case 'PUT': {
        const updateData = req.body;
        
        try {
          const updatedNPC = await NPC.findByIdAndUpdate(
            id,
            updateData,
            {
              new: true,
              runValidators: true,
              context: 'query'
            }
          );

          if (!updatedNPC) {
            return res.status(404).json({ error: 'NPC not found' });
          }

          return res.status(200).json(updatedNPC);
        } catch (validationError: any) {
          return res.status(400).json({
            error: 'Validation failed',
            details: validationError.errors
          });
        }
      }

      case 'DELETE': {
        const npc = await NPC.findById(id);
        if (!npc) {
          return res.status(404).json({ error: 'NPC not found' });
        }

        // Delete associated profile image if it exists
        if (npc.profileImage) {
          const fileName = npc.profileImage.split('/').pop();
          if (fileName) {
            await deleteImage(fileName);
          }
        }

        await NPC.findByIdAndDelete(id);
        return res.status(200).json({ message: 'NPC deleted successfully' });
      }

      default:
        res.setHeader('Allow', ['GET', 'PUT', 'PATCH', 'DELETE']);
        return res.status(405).json({ error: `Method ${method} not allowed` });
    }
  } catch (error: any) {
    console.error('API Error:', error);
    
    if (error.name === 'ValidationError') {
      return res.status(400).json({
        error: 'Validation failed',
        details: error.errors
      });
    }
    
    if (error.name === 'CastError') {
      return res.status(400).json({
        error: 'Invalid ID format'
      });
    }
    
    return res.status(500).json({
      error: 'Internal server error',
      message: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
}
