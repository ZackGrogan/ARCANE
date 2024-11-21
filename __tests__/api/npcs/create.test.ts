import { createMocks } from 'node-mocks-http';
import createNPCHandler from '../../../pages/api/npcs/create';
import connectToDatabase from '../../../utils/mongodb';
import mongoose from 'mongoose';

jest.mock('../../../utils/mongodb', () => ({
  __esModule: true,
  default: jest.fn(),
}));

jest.mock('mongoose', () => ({
  ...jest.requireActual('mongoose'),
  model: jest.fn().mockReturnValue({
    save: jest.fn().mockResolvedValue({
      name: 'Thorin Oakenshield',
      race: 'Dwarf',
      class: 'Warrior',
    }),
  }),
}));

jest.setTimeout(10000);

beforeAll(async () => {
  (connectToDatabase as jest.Mock).mockResolvedValue(true);
});

afterAll(async () => {
  jest.clearAllMocks();
});

describe('/api/npcs/create API Endpoint', () => {
  test('should create a new NPC', async () => {
    const { req, res } = createMocks({
      method: 'POST',
      body: {
        name: 'Thorin Oakenshield',
        race: 'Dwarf',
        class: 'Warrior',
      },
    });

    await createNPCHandler(req, res);

    expect(res._getStatusCode()).toBe(201);
    const data = JSON.parse(res._getData());
    expect(data.name).toBe('Thorin Oakenshield');
  });

  test('should return 405 if method is not POST', async () => {
    const { req, res } = createMocks({
      method: 'GET',
    });

    await createNPCHandler(req, res);

    expect(res._getStatusCode()).toBe(405);
  });
});
