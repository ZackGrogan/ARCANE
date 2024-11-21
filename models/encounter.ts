import mongoose, { Document, Schema } from 'mongoose';

interface Encounter extends Document {
  title: string;
  description: string;
  monsters: string[];
  tactics: string[];
  biome: string;
  weather: string;
  hazards: string[];
  loot: string[];
  roleplayingScenarios: string[];
  difficulty: string;
  createdAt: Date;
  updatedAt: Date;
}

const EncounterSchema: Schema = new Schema(
  {
    title: { type: String, required: true },
    description: { type: String, required: true },
    monsters: { type: [String], default: [] },
    tactics: { type: [String], default: [] },
    biome: { type: String, required: true },
    weather: { type: String, required: true },
    hazards: { type: [String], default: [] },
    loot: { type: [String], default: [] },
    roleplayingScenarios: { type: [String], default: [] },
    difficulty: { type: String, required: true },
  },
  { timestamps: true }
);

export default mongoose.model<Encounter>('Encounter', EncounterSchema);
