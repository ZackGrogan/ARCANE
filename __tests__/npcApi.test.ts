import request from 'supertest';
import app from '../app';
import { NPC } from '../models/npc';
import { uploadImage } from '../services/imageStorageService';

jest.mock('../services/imageStorageService');

const mockNpcData = {
  name: 'Test NPC',
  race: 'Elf',
  class: 'Wizard',
  skills: ['Magic'],
  equipment: ['Staff']
};

beforeEach(() => {
  jest.clearAllMocks();
});

describe('NPC API', () => {
  it('should update NPC with a new profile image', async () => {
    (uploadImage as jest.Mock).mockResolvedValue('https://example.com/new-image.png');

    const npc = new NPC(mockNpcData);
    await npc.save();

    const response = await request(app)
      .patch(`/api/npcs/${npc._id}`)
      .field('name', 'Updated NPC')
      .attach('profileImage', Buffer.from('test image data'), 'profile.png');

    expect(response.status).toBe(200);
    expect(response.body.profileImage).toBe('https://example.com/new-image.png');
    expect(uploadImage).toHaveBeenCalled();
  });
});
