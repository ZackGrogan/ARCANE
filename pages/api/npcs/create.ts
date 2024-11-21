import { NextApiRequest, NextApiResponse } from 'next';
import connectToDatabase from '../../../utils/mongodb';
import { NPC } from '@models/npc';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    await connectToDatabase();
    try {
      const npc = new NPC(req.body);
      await npc.save();
      res.status(201).json(npc);
    } catch (error) {
      res.status(400).json({ message: 'Error creating NPC', error });
    }
  } else {
    res.status(405).json({ message: 'Method not allowed' });
  }
}
