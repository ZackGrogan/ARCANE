import { createMocks } from 'node-mocks-http';
import handler from '@/pages/api/npcs';
import connectToDatabase from '@/utils/mongodb';
import NPC from '@/models/npc';

jest.mock('@/utils/mongodb', () => ({
  connectToDatabase: jest.fn(),
}));

describe('/api/npcs', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should return all NPCs', async () => {
    const mockNPCs = [
      {
        name: 'Test NPC 1',
        race: 'Human',
        class: 'Fighter',
        background: 'Soldier',
        alignment: 'Lawful Good',
        personalityTraits: 'Brave and loyal',
        backstory: 'A veteran of many battles',
        appearance: 'Tall and muscular',
        skills: ['Athletics', 'Intimidation'],
        equipment: ['Longsword', 'Shield'],
      },
      {
        name: 'Test NPC 2',
        race: 'Elf',
        class: 'Wizard',
        background: 'Sage',
        alignment: 'Neutral Good',
        personalityTraits: 'Wise and patient',
        backstory: 'Studied at a prestigious academy',
        appearance: 'Slender with silver hair',
        skills: ['Arcana', 'History'],
        equipment: ['Staff', 'Spellbook'],
      },
    ];

    // Mock the NPC.find() method
    NPC.find = jest.fn().mockResolvedValue(mockNPCs);

    const { req, res } = createMocks({
      method: 'GET',
    });

    await handler(req, res);

    expect(res._getStatusCode()).toBe(200);
    expect(JSON.parse(res._getData())).toEqual(mockNPCs);
    expect(connectToDatabase).toHaveBeenCalled();
  });

  it('should handle errors gracefully', async () => {
    const error = new Error('Database error');
    NPC.find = jest.fn().mockRejectedValue(error);

    const { req, res } = createMocks({
      method: 'GET',
    });

    await handler(req, res);

    expect(res._getStatusCode()).toBe(500);
    expect(JSON.parse(res._getData())).toEqual({
      error: 'Failed to fetch NPCs',
    });
  });

  it('should return 405 for non-GET methods', async () => {
    const { req, res } = createMocks({
      method: 'POST',
    });

    await handler(req, res);

    expect(res._getStatusCode()).toBe(405);
    expect(JSON.parse(res._getData())).toEqual({
      error: 'Method not allowed',
    });
  });
});
