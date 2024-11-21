import mongoose, { Document, Schema } from 'mongoose';

interface Encounter extends Document {
  title: string;
  description: string;
  monsters: { name: string; quantity: number }[];
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
    title: { 
      type: String, 
      required: true,
      index: true, 
      maxLength: 100
    },
    description: { 
      type: String, 
      required: true,
      maxLength: 1000
    },
    monsters: [{
      name: { type: String, required: true },
      quantity: { 
        type: Number, 
        required: true,
        min: 1,
        max: 100
      }
    }],
    tactics: { type: [String], default: [] },
    biome: { type: String, required: true },
    weather: { type: String, required: true },
    hazards: { type: [String], default: [] },
    loot: { type: [String], default: [] },
    roleplayingScenarios: { type: [String], default: [] },
    difficulty: {
      type: String,
      required: true,
      enum: ['Trivial', 'Easy', 'Medium', 'Hard', 'Deadly'],
      index: true
    },
    createdAt: { type: Date, default: Date.now, index: true },
    updatedAt: { type: Date, default: Date.now }
  },
  { timestamps: true }
);

// Indexing for performance
EncounterSchema.index({ title: 1 });
EncounterSchema.index({ difficulty: 1 });

export default mongoose.model<Encounter>('Encounter', EncounterSchema);
