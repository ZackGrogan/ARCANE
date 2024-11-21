import { NextApiRequest, NextApiResponse } from 'next';
import dbConnect from '@/lib/dbConnect';
import Encounter from '@/models/encounter';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { method } = req;

  await dbConnect();

  switch (method) {
    case 'GET':
      try {
        const encounters = await Encounter.find({});
        res.status(200).json(encounters);
      } catch (error) {
        console.error('Error fetching encounters:', error);
        res.status(500).json({ error: 'Error fetching encounters' });
      }
      break;
    case 'POST':
      try {
        const encounter = new Encounter(req.body);
        await encounter.save();
        res.status(201).json(encounter);
      } catch (error) {
        console.error('Error creating encounter:', error);
        res.status(400).json({ error: 'Error creating encounter' });
      }
      break;
    default:
      res.setHeader('Allow', ['GET', 'POST']);
      res.status(405).end(`Method ${method} Not Allowed`);
      break;
  }
}
