import axios from 'axios';

const HUGGING_FACE_API_KEY = process.env.HUGGING_FACE_API_KEY;
const HUGGING_FACE_API_URL = 'https://api-inference.huggingface.co/models/flux';

// Removed console log for API key
if (!HUGGING_FACE_API_KEY) {
  throw new Error('Hugging Face API Key is not set in the environment variables.');
}

export const generateProfilePicture = async (prompt: string): Promise<Blob> => {
  try {
    const response = await axios.post(
      HUGGING_FACE_API_URL,
      { inputs: prompt },
      {
        headers: {
          'Authorization': `Bearer ${HUGGING_FACE_API_KEY}`,
          'Content-Type': 'application/json'
        },
        responseType: 'blob',
      }
    );

    if (response.status !== 200) {
      throw new Error(`Failed to generate image: ${response.statusText}`);
    }

    return response.data;
  } catch (error) {
    console.error('Error generating profile picture:', {
      error,
      prompt,
      apiUrl: HUGGING_FACE_API_URL
    });
    throw error;
  }
};
