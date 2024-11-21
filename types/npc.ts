export interface NPC {
  _id?: string;
  name: string;
  race: string;
  class: string;
  backstory?: string;
  personalityTraits?: string;
  appearance?: string;
  skills: string[];
  equipment: string[];
  createdAt?: Date;
  updatedAt?: Date;
}
