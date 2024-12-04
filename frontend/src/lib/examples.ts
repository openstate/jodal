const examples = [
  {
    name: "Windmolens in Noord-Holland",
    emoji: "🌬️",
    query: "windmolens&organisaties=PV27",
  },
  {
    name: "Sociale huur in Rotterdam",
    query: '"sociale huur"&organisaties=GM0599',
    emoji: "🏠",
  },
  {
    name: "Onderwijs in Utrecht",
    query: "onderwijs&organisaties=GM0344",
    emoji: "📚",
  },
  {
    name: "Vergrijzing in Limburg",
    query: "vergrijzing&organisaties=PV31",
    emoji: "🧓",
  },
  {
    name: "Fietsbeleid in Amsterdam",
    query:
      "fiets | fietsers | fietsen&organisaties=GM0363,GM0363S56,GM0363S90,GM0363S10,GM0363S88,GM0363S91,GM0363S89,GM0363S17",
    emoji: "🚲",
  },
  {
    name: "Waterveiligheid in Zeeland",
    query: "waterveiligheid | overstroming | dijk | kering&organisaties=PV29",
    emoji: "🌊",
  },

  {
    name: "Monumenten in Leiden",
    query: "monumenten&organisaties=GM0546",
    emoji: "🏛️",
  },
  {
    name: "Bosbeheer in Gelderland",
    query: "bosbeheer | bos | bossen | bomen&organisaties=PV25",
    emoji: "🌳",
  },
  {
    name: "Toerisme op Texel",
    query: "toerisme | toeristen&organisaties=GM0448",
    emoji: "🏖️",
  },
  {
    name: "Cultuur in Maastricht",
    query: "cultuur&organisaties=GM0935",
    emoji: "🎭",
  },
  {
    name: "Toegankelijkheid",
    query: "toegankelijkheid",
    emoji: "♿",
  },
  {
    name: "Cybercriminaliteit",
    query: "cybercrime | cybercriminaliteit | cybersecurity",
    emoji: "🛡️",
  },
  {
    name: "Luchtkwaliteit",
    query: 'luchtkwaliteit | "schone lucht"',
    emoji: "🌫️",
  },
  {
    name: "Zwerfafval",
    query: "zwerfafval",
    emoji: "🗑️",
  },
  {
    name: "Digitalisering",
    query: "digitalisering | ICT | cloud",
    emoji: "💻",
  },
  {
    name: "Verkeersveiligheid",
    query: "verkeersveiligheid",
    emoji: "🚦",
  },
  {
    name: "Warmtevisie",
    query: "warmtevisie",
    emoji: "🌡️",
  },
  {
    name: "Transparantie",
    query: "transparantie | geheimhouding | WOO",
    emoji: "🔍",
  },
  {
    name: "Diversiteit",
    query: "diversiteit | inclusiviteit",
    emoji: "🌈",
  },
  {
    name: "Gezondheid",
    query: "zorg | gezondheid | ziekenhuis | huisarts",
    emoji: "🏥",
  },
  {
    name: "Energietransitie",
    query: "energietransitie",
    emoji: "🔋",
  },
  {
    name: "Woningbouw",
    query: "woningbouw",
    emoji: "🏗️",
  },
  {
    name: "Mobiliteit",
    query: "mobiliteit",
    emoji: "🚗",
  },
  {
    name: "Werkgelegenheid",
    query: "werkgelegenheid | banen | werk",
    emoji: "👩‍💼",
  },
  {
    name: "Veiligheid",
    query: "veiligheid | veilig",
    emoji: "🦺",
  },
];

function pickRandom<T>(array: T[], n: number): T[] {
  return array.sort(() => 0.5 - Math.random()).slice(0, n);
}

export function getRandomExamples() {
  return pickRandom(examples, 6);
}
