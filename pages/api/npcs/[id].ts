import { NextApiRequest, NextApiResponse } from 'next';
import { dbConnect } from '@/lib/dbConnect';
import { NPC } from '@/models/npc';
import { isValidObjectId } from 'mongoose';

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
        const updateData = req.body;
        
        // Validate the update data
        const npc = await NPC.findById(id);
        if (!npc) {
          return res.status(404).json({ error: 'NPC not found' });
        }

        // Update only the fields that are provided
        Object.keys(updateData).forEach(key => {
          if (updateData[key] !== undefined) {
            npc[key] = updateData[key];
          }
        });

        try {
          await npc.validate();
        } catch (validationError: any) {
          return res.status(400).json({
            error: 'Validation failed',
            details: validationError.errors
          });
        }

        const updatedNPC = await npc.save();
        return res.status(200).json(updatedNPC);
      }

      case 'PUT': {
        const updateData = req.body;
        
        try {
          const updatedNPC = await NPC.findByIdAndUpdate(
            id,
            updateData,
            {
              new: true, // Return the updated document
              runValidators: true, // Run schema validators
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
        const deletedNPC = await NPC.findByIdAndDelete(id);
        
        if (!deletedNPC) {
          return res.status(404).json({ error: 'NPC not found' });
        }

        return res.status(200).json({ message: 'NPC deleted successfully' });
      }

      default:
        res.setHeader('Allow', ['GET', 'PUT', 'PATCH', 'DELETE']);
        return res.status(405).json({ error: `Method ${method} not allowed` });
    }
  } catch (error: any) {
    console.error('API Error:', error);
    
    // Handle specific error types
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
