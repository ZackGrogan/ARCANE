import { NextApiRequest, NextApiResponse } from 'next';
import connectToDatabase from '../../../utils/mongodb';
import { NPC } from '../../../models/npc';

export default async function handler(_req: NextApiRequest, res: NextApiResponse) {
  await connectToDatabase();
  try {
    const npcs = await NPC.find({});
    res.status(200).json(npcs);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching NPCs', error });
  }
}
