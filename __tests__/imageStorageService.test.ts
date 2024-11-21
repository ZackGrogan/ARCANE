import { uploadImage, deleteImage } from '../services/imageStorageService';
import AWS from 'aws-sdk';

jest.mock('aws-sdk', () => {
  const mS3 = {
    upload: jest.fn().mockReturnThis(),
    promise: jest.fn().mockResolvedValue({ Location: 'https://example.com/image.png' }),
    deleteObject: jest.fn().mockReturnThis()
  };
  return { S3: jest.fn(() => mS3) };
});

const mockFileBuffer = Buffer.from('test image data');
const mockFileType = 'image/png';

describe('Image Storage Service', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should upload an image and return the URL', async () => {
    const url = await uploadImage(mockFileBuffer, mockFileType);
    expect(url).toBe('https://example.com/image.png');
    expect(AWS.S3.prototype.upload).toHaveBeenCalledWith(expect.objectContaining({
      Body: mockFileBuffer,
      ContentType: mockFileType
    }));
  });

  it('should delete an image', async () => {
    await deleteImage('image.png');
    expect(AWS.S3.prototype.deleteObject).toHaveBeenCalledWith(expect.objectContaining({
      Key: 'image.png'
    }));
  });
});
