import { uploadImage, deleteImage, getImagePath } from '../services/localStorageService';
import fs from 'fs';
import path from 'path';

jest.mock('fs', () => ({
  promises: {
    writeFile: jest.fn(),
    unlink: jest.fn(),
  },
  existsSync: jest.fn(),
  mkdirSync: jest.fn(),
}));

describe('Local Storage Service', () => {
  const mockBuffer = Buffer.from('test image data');
  const mockFileType = 'image/png';

  beforeEach(() => {
    jest.clearAllMocks();
    (fs.existsSync as jest.Mock).mockReturnValue(true);
  });

  it('should upload an image and return the URL', async () => {
    const url = await uploadImage(mockBuffer, mockFileType);
    expect(url).toMatch(/^\/uploads\/[\w-]+\.png$/);
    expect(fs.promises.writeFile).toHaveBeenCalledWith(
      expect.stringContaining('uploads'),
      mockBuffer
    );
  });

  it('should delete an image', async () => {
    const fileName = 'test.png';
    (fs.existsSync as jest.Mock).mockReturnValue(true);
    
    await deleteImage(fileName);
    
    expect(fs.promises.unlink).toHaveBeenCalledWith(
      expect.stringContaining(fileName)
    );
  });

  it('should not throw when deleting non-existent image', async () => {
    const fileName = 'nonexistent.png';
    (fs.existsSync as jest.Mock).mockReturnValue(false);
    
    await expect(deleteImage(fileName)).resolves.not.toThrow();
    expect(fs.promises.unlink).not.toHaveBeenCalled();
  });

  it('should return correct image path', () => {
    const fileName = 'test.png';
    const imagePath = getImagePath(fileName);
    expect(imagePath).toContain('uploads');
    expect(imagePath).toContain(fileName);
  });
});
