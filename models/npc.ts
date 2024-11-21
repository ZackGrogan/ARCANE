import mongoose, { Document, Schema } from 'mongoose';

export interface NPCDocument extends Document {
  name: string;
  race: string;
  class: string;
  backstory?: string;
  personalityTraits?: string;
  appearance?: string;
  skills: string[];
  equipment: string[];
  createdAt: Date;
  updatedAt: Date;
}

const NPCSchema = new Schema({
  name: { 
    type: String, 
    required: [true, 'Name is required'],
    trim: true,
    minlength: [2, 'Name must be at least 2 characters long'],
    maxlength: [100, 'Name cannot be longer than 100 characters']
  },
  race: { 
    type: String, 
    required: [true, 'Race is required'],
    trim: true,
    minlength: [2, 'Race must be at least 2 characters long'],
    maxlength: [50, 'Race cannot be longer than 50 characters']
  },
  class: { 
    type: String, 
    required: [true, 'Class is required'],
    trim: true,
    minlength: [2, 'Class must be at least 2 characters long'],
    maxlength: [50, 'Class cannot be longer than 50 characters']
  },
  backstory: {
    type: String,
    trim: true,
    maxlength: [10000, 'Backstory cannot be longer than 10000 characters']
  },
  personalityTraits: {
    type: String,
    trim: true,
    maxlength: [2000, 'Personality traits cannot be longer than 2000 characters']
  },
  appearance: {
    type: String,
    trim: true,
    maxlength: [2000, 'Appearance description cannot be longer than 2000 characters']
  },
  skills: {
    type: [String],
    default: [],
    validate: {
      validator: function(v: string[]) {
        return v.every(skill => skill.length >= 1 && skill.length <= 100);
      },
      message: 'Each skill must be between 1 and 100 characters'
    }
  },
  equipment: {
    type: [String],
    default: [],
    validate: {
      validator: function(v: string[]) {
        return v.every(item => item.length >= 1 && item.length <= 100);
      },
      message: 'Each equipment item must be between 1 and 100 characters'
    }
  }
}, {
  timestamps: true, // Adds createdAt and updatedAt fields
  toJSON: { 
    virtuals: true,
    transform: function(doc, ret) {
      ret.id = ret._id;
      delete ret._id;
      delete ret.__v;
      return ret;
    }
  }
});

// Add text index for search functionality
NPCSchema.index({ 
  name: 'text', 
  race: 'text', 
  class: 'text',
  backstory: 'text',
  personalityTraits: 'text'
});

// Pre-save middleware to sanitize text fields
NPCSchema.pre('save', function(next) {
  // Basic XSS prevention
  const sanitize = (str: string) => {
    if (!str) return str;
    return str
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  };

  this.name = sanitize(this.name);
  this.race = sanitize(this.race);
  this.class = sanitize(this.class);
  
  if (this.skills) {
    this.skills = this.skills.map(sanitize);
  }
  if (this.equipment) {
    this.equipment = this.equipment.map(sanitize);
  }

  next();
});

export const NPC = mongoose.models.NPC || mongoose.model<NPCDocument>('NPC', NPCSchema);
