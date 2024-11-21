// Name generation utilities for different D&D 5e races
const namePatterns = {
  dragonborn: {
    prefixes: ['Ar', 'Bala', 'Dra', 'Gher', 'Kri', 'Mor', 'Nar', 'Sar', 'Tor', 'Zor'],
    suffixes: ['sar', 'thor', 'don', 'kas', 'mil', 'rax', 'thax', 'zar', 'dis', 'nix']
  },
  dwarf: {
    prefixes: ['Bael', 'Dain', 'Duer', 'Grun', 'Thor', 'Torg', 'Thar', 'Kild', 'Mor', 'Bar'],
    suffixes: ['dim', 'grim', 'gar', 'dain', 'thor', 'rim', 'din', 'dur', 'gin', 'mir']
  },
  elf: {
    prefixes: ['Aer', 'Cal', 'Eres', 'Gala', 'Lum', 'Mor', 'Sil', 'Var', 'Xan', 'Yen'],
    suffixes: ['ion', 'riel', 'wen', 'thor', 'dril', 'las', 'ril', 'sor', 'mir', 'nil']
  },
  human: {
    prefixes: ['Al', 'Ber', 'Car', 'Dan', 'Ed', 'Fre', 'Ger', 'Hen', 'Ian', 'Jak'],
    suffixes: ['ard', 'win', 'ton', 'ric', 'mer', 'ley', 'son', 'wick', 'ford', 'mont']
  },
  tiefling: {
    prefixes: ['Ash', 'Brim', 'Cinder', 'Doom', 'Fell', 'Grim', 'Hex', 'Mal', 'Sin', 'Woe'],
    suffixes: ['fire', 'heart', 'blood', 'soul', 'dark', 'pain', 'fear', 'spite', 'rage', 'sin']
  }
};

export function generateName(race?: string, prompt?: string): string {
  // If a prompt is provided, use it to influence name generation
  if (prompt) {
    // TODO: Implement more sophisticated prompt-based name generation
    return prompt;
  }

  // Default to human if no race is specified or race is not in patterns
  const pattern = namePatterns[race?.toLowerCase() || 'human'] || namePatterns.human;
  
  const prefix = pattern.prefixes[Math.floor(Math.random() * pattern.prefixes.length)];
  const suffix = pattern.suffixes[Math.floor(Math.random() * pattern.suffixes.length)];
  
  return prefix + suffix;
}
