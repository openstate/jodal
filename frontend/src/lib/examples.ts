const examples = [
  {
    name: "Windmolens in Noord-Holland",
    query: "windmolens&organisaties=PV27",
  },
  {
    name: "Sociale huur in Rotterdam",
    query: '"sociale huur"&organisaties=GM0599',
  },
  {
    name: "Onderwijs in Utrecht",
    query: "onderwijs&organisaties=GM0344",
  },
  {
    name: "Vergrijzing in Limburg",
    query: "vergrijzing&organisaties=PV31",
  },
  {
    name: "Fietsbeleid in Amsterdam",
    query:
      "fiets&organisaties=GM0363,GM0363S56,GM0363S90,GM0363S10,GM0363S88,GM0363S91,GM0363S89,GM0363S17",
  },
  {
    name: "Waterveiligheid in Zeeland",
    query: "waterveiligheid&organisaties=PV29",
  },
  {
    name: "Monumenten in Leiden",
    query: "monumenten&organisaties=GM0546",
  },
  {
    name: "Bosbeheer in Gelderland",
    query: "bosbeheer&organisaties=PV25",
  },
  {
    name: "Toerisme op Texel",
    query: "toerisme&organisaties=GM0448",
  },
  {
    name: "Cultuur in Maastricht",
    query: "cultuur&organisaties=GM0935",
  },
  {
    name: "Toegankelijkheid",
    query: "toegankelijkheid",
  },
  {
    name: "Cybercrime",
    query: "cybercrime",
  },
  {
    name: "Luchtkwaliteit",
    query: 'luchtkwaliteit',
  },
  {
    name: "Zwerfafval",
    query: "zwerfafval",
  },
  {
    name: "Digitalisering",
    query: "digitalisering",
  },
  {
    name: "Verkeersveiligheid",
    query: "verkeersveiligheid",
  },
  {
    name: "Warmtevisie",
    query: "warmtevisie",
  },
  {
    name: "Transparantie",
    query: "transparantie",
  },
  {
    name: "Diversiteit",
    query: "diversiteit",
  },
  {
    name: "Gezondheid",
    query: "gezondheid",
  },
  {
    name: "Energietransitie",
    query: "energietransitie",
  },
  {
    name: "Woningbouw in Den Haag",
    query: "woningbouw&organisaties=GM0518",
  },
  {
    name: "Mobiliteit in Breda",
    query: "mobiliteit&organisaties=GM0758",
  },
  {
    name: "Werkgelegenheid",
    query: "werkgelegenheid",
  },
  {
    name: "Veiligheid in Zwolle",
    query: "veiligheid&organisaties=GM0193",
  },
];

function pickRandom<T>(array: T[], n: number): T[] {
  return array.sort(() => 0.5 - Math.random()).slice(0, n);
}

export function getRandomExamples() {
  return pickRandom(examples, 6);
}
