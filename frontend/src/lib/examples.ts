const examples = [
  { name: "Windmolens in Eemshaven", emoji: "🌬️" },
  { name: "Sociale huur in Rotterdam", emoji: "🏠" },
  { name: "Onderwijs in Utrecht", emoji: "📚" },
  { name: "Vergrijzing in Limburg", emoji: "🧓" },
  { name: "Fietsbeleid in Amsterdam", emoji: "🚲" },
  { name: "Waterveiligheid in Zeeland", emoji: "🌊" },
  { name: "Monumenten in Leiden", emoji: "🏛️" },
  { name: "Toegankelijkheid", emoji: "♿" },
  { name: "Bosbeheer in Gelderland", emoji: "🌳" },
  { name: "Toerisme op Texel", emoji: "🏖️" },
  { name: "Cultuur in Maastricht", emoji: "🎭" },
  { name: "Cybercriminaliteit", emoji: "🛡️" },
  { name: "Luchtkwaliteit", emoji: "🌫️" },
  { name: "Zwerfafval", emoji: "🗑️" },
  { name: "Digitalisering", emoji: "💻" },
  { name: "Verkeersveiligheid", emoji: "🚦" },
  { name: "Warmtevisie", emoji: "🌡️" },
  { name: "Transparantie", emoji: "🔍" },
  { name: "Diversiteit", emoji: "🌈" },
  { name: "Gezondheid", emoji: "🏥" },
  { name: "Energietransitie", emoji: "🔋" },
  { name: "Woningbouw", emoji: "🏗️" },
  { name: "Mobiliteit", emoji: "🚗" },
  { name: "Werkgelegenheid", emoji: "👩‍💼" },
  { name: "Veiligheid", emoji: "🦺" },
];

function pickRandom<T>(array: T[], n: number): T[] {
  return array.sort(() => 0.5 - Math.random()).slice(0, n);
}

export function getRandomExamples() {
  return pickRandom(examples, 6);
}
