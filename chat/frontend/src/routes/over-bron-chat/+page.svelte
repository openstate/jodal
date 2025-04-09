# Create new file
<script>
  import { page } from '$app/stores';
</script>

<svelte:head>
  <title>Bron chat - Over ons</title>
</svelte:head>

<div class="container mx-auto px-4 pt-32 pb-8 max-w-4xl">
  <h1 class="text-3xl font-bold mb-8">Over Bron chat</h1>
  
  <div class="space-y-8">
    <!-- Introductie -->
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <p class="text-gray-700 mb-4">
        Bron chat is een tool voor journalisten en onderzoekers. 
        Onze missie: openbare overheidsinformatie makkelijk en snel doorzoekbaar maken door middel van een AI chat.
        Dagelijks werken wij aan het uitbreiden en verbeteren van Bron chat. De tool is op het moment in beta.
      </p>
      <p class="text-gray-700 mb-4">
        Bron chat is tot stand gekomen tijdens de SVDJ Incubator 2024-2025. De SVDJ Incubator is een subsidie- en begeleidingsprogramma van het Stimuleringsfonds voor de Journalistiek (SVDJ) gericht op het vinden van oplossingen voor gedeelde vraagstukken binnen de journalistieke sector. 

        Het SVDJ stimuleert met kennisdeling, begeleiding en subsidie een onafhankelijke, diverse en toekomstbestendige journalistieke infrastructuur in Nederland. 
        
        Voor vragen over de SVDJ Incubator of de oplossingen die hieruit voort zijn gekomen, ga naar <a href="https://www.svdj.nl/incubator" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">www.svdj.nl/incubator</a>. 
      
        <a href="https://www.svdj.nl/incubator" target="_blank" rel="noopener noreferrer">
            <img src="/svdj-incubator-official.png" alt="SVDJ Incubator" class="w-2/3 mx-auto">
        </a>
    </p>
    </div>

    <!-- Wat Bron chat biedt -->
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-2xl font-semibold mb-4">Wat Bron chat biedt</h2>
      <ul class="list-disc text-gray-700 space-y-3 pl-8">
        <li>
          <strong>Nieuwe inzichten dankzij AI:</strong> Ontdek verbanden en patronen in overheidsdata.
        </li>
        <li>
          <strong>Miljoenen documenten:</strong> Doorzoek 3,5 miljoen overheidsdocumenten op één centrale plek.
        </li>
        <li>
          <strong>Bronverwijzingen:</strong> Directe links naar originele documenten en downloadbare pdf's.
        </li>
        <li>
          <strong>Samenwerking:</strong> Deel je zoekresultaten eenvoudig met collega's via deelbare links.
        </li>
        <li>
          <strong>Transparante data:</strong> Ontsloten door Open State Foundation, een onafhankelijke stichting zonder winstoogmerk.
        </li>
        <li>
          <strong>Speciaal voor journalisten:</strong> Een betrouwbare, flexibele tool ontwikkeld door SVDJ Incubator, onderdeel van het Stimuleringsfonds voor de Journalistiek.
        </li>
      </ul>
    </div>

    <!-- Team -->
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-2xl font-semibold mb-4">Het team</h2>
      <p class="text-gray-700 mb-4">
        Bron chat is ontwikkeld door een team van SVDJ Incubator dat bestaat uit Jeremy Crowlesmith, Henri Bouwmeester en Joost van de Loo.
        Bron chat maakt gebruik van de data van Bron, een product van Open State Foundation.
      </p>
      <p class="text-gray-700">
        Eind maart 2025, als SVDJ het project open sourced, neemt Open State Foundation het beheer en de verdere ontwikkeling van Bron chat over.
      </p>
    </div>

    <!-- Toekomstvisie -->
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-2xl font-semibold mb-4">Onze visie</h2>
      <p class="text-gray-700 mb-4">
        Bron chat democratiseert het doen van onderzoek, doordat zoeken in openbare overheidsdata nu flexibel en makkelijk wordt 
        voor alle soorten journalisten en onderzoekers, zowel landelijk als in de regio. Hierdoor kan de journalistiek met minder middelen meer bereiken.
      </p>
      <p class="text-gray-700">
        Onze visie voor Bron chat, en diensten die er mogelijk in de toekomst nog bij gaan komen,
        is dat iedere journalist in Nederland moet kunnen onderzoeken op een hoog niveau.
      </p>
    </div>

    <!-- Steun ons -->
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-2xl font-semibold mb-4">Steun ons</h2>
      <p class="text-gray-700 mb-4">
        Tot eind maart 2025 wordt Bron chat als prototype ondersteund door de SVDJ Incubator.
        Daarna wordt het overgenomen als een dienst van Open State Foundation, en daarmee afhankelijk van donaties.
      </p>
      <p class="text-gray-700 mb-4">
        Ben je er net als wij van overtuigd dat iedereen vrij moet kunnen beschikken over vitale overheidsinformatie
        over bijvoorbeeld het onderwijs, de zorg of het klimaat?
        Steun dan Open State Foundation in haar missie voor digitale transparantie bij de overheid.
      </p>
      <!-- <div class="mt-4">
        <a
          href="https://openstate.eu/nl/doneren/"
          class="inline-block bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors"
          target="_blank"
          rel="noopener noreferrer"
        >
          Doneer aan Open State Foundation
        </a>
      </div> -->
    </div>
  </div>
</div> 