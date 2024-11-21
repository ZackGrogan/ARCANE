import fs from 'fs';
import path from 'path';
import { v4 as uuidv4 } from 'uuid';

const UPLOAD_DIR = path.join(process.cwd(), 'public', 'uploads');

// Ensure upload directory exists
if (!fs.existsSync(UPLOAD_DIR)) {
  fs.mkdirSync(UPLOAD_DIR, { recursive: true });
}

export const uploadImage = async (file: Buffer, fileType: string): Promise<string> => {
  const fileName = `${uuidv4()}.${fileType.split('/')[1]}`;
  const filePath = path.join(UPLOAD_DIR, fileName);

  try {
    await fs.promises.writeFile(filePath, file);
    // Return the public URL for the image
    return `/uploads/${fileName}`;
  } catch (error) {
    console.error('Error uploading image:', error);
    throw error;
  }
};

export const deleteImage = async (fileName: string): Promise<void> => {
  if (!fileName) return;

  const filePath = path.join(UPLOAD_DIR, path.basename(fileName));

  try {
    if (fs.existsSync(filePath)) {
      await fs.promises.unlink(filePath);
    }
  } catch (error) {
    console.error('Error deleting image:', error);
    throw error;
  }
};

export const getImagePath = (fileName: string): string => {
  return path.join(UPLOAD_DIR, fileName);
};
