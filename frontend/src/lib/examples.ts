const examples = [
  {
    name: "Windmolens in Noord-Holland",
    query: "windmolens&organisaties=PV27",
  },
  {
    name: "Sociale huur in Zoetermeer",
    query: "sociale huur&organisaties=GM0637",
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
    query: "fiets&organisaties=GM0363",
  },
  {
    name: "Haven in Rotterdam",
    query: "haven&organisaties=GM0599",
  },
  {
    name: "Monumenten in Groningen",
    query: "monumenten&organisaties=GM0014",
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
    name: "Bouw in Den Haag",
    query: "Bouw&organisaties=GM0518",
  },
  {
    name: "Mobiliteit in Breda",
    query: "mobiliteit&organisaties=GM0758",
  },

  {
    name: "Veiligheid in Zwolle",
    query: "veiligheid&organisaties=GM0193",
  },
  {
    name: "Natuur in Zutphen",
    query: "natuur&organisaties=GM0301",
  },
  {
    name: "Werkgelegenheid",
    query: "werkgelegenheid",
  },
  {
    name: "Toegankelijkheid in Enschede",
    query: "toegankelijkheid&organisaties=GM0153",
  },
  {
    name: "Luchtkwaliteit in Rheden",
    query: "luchtkwaliteit&organisaties=GM0275",
  },
  {
    name: "Digitalisering in Apeldoorn",
    query: "digitalisering&organisaties=GM0200",
  },
  {
    name: "Zwerfafval",
    query: "zwerfafval",
  },
  {
    name: "Cybercrime",
    query: "cybercrime",
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
];

function pickRandom<T>(array: T[], n: number): T[] {
  return array.sort(() => 0.5 - Math.random()).slice(0, n);
}

export function getRandomExamples() {
  return pickRandom(examples, 6);
}
