import mongoose, { Document, Schema } from 'mongoose';

export interface NPCDocument extends Document {
  name: string;
  race: string;
  class: string;
}

const NPCSchema = new Schema({
  name: { type: String, required: true },
  race: { type: String, required: true },
  class: { type: String, required: true },
});

export const NPC = mongoose.model<NPCDocument>('NPC', NPCSchema);
