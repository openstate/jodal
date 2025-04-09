<script>
  import { page } from '$app/stores';
</script>

<svelte:head>
  <title>Bron chat - Veel gestelde vragen</title>
</svelte:head>

<div class="container mx-auto px-4 pt-32 pb-8 max-w-4xl">
  <h1 class="text-3xl font-bold mb-8">Veel gestelde vragen</h1>
  
  <div class="space-y-4">
  
    <!-- FAQ Items -->
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-xl font-semibold mb-2">Wie zit er achter Bron chat?</h2>
      <p class="text-gray-700 mb-4">
        Bron chat is ontwikkeld door een team van SVDJ Incubator dat bestaat uit Jeremy Crowlesmith, Henri Bouwmeester en Joost van de Loo.
        Bron chat maakt gebruik van de data van Bron, een product van Open State Foundation.
        Open State Foundation zal vanaf maart 2025 het beheer en onderhoud van Bron chat overnemen.
      </p>
      <p class="text-gray-700 mb-4">
        Bron chat is tot stand gekomen tijdens de SVDJ Incubator 2024-2025. De SVDJ Incubator is een subsidie- en begeleidingsprogramma van het Stimuleringsfonds voor de Journalistiek (SVDJ) gericht op het vinden van oplossingen voor gedeelde vraagstukken binnen de journalistieke sector. 

        Het SVDJ stimuleert met kennisdeling, begeleiding en subsidie een onafhankelijke, diverse en toekomstbestendige journalistieke infrastructuur in Nederland. 
        
        Voor vragen over de SVDJ Incubator of de oplossingen die hieruit voort zijn gekomen, ga naar <a href="https://www.svdj.nl/incubator" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">www.svdj.nl/incubator</a>. 

        <a href="https://www.svdj.nl/incubator" target="_blank" rel="noopener noreferrer">
            <img src="/svdj-incubator-official.png" alt="SVDJ Incubator" class="w-2/3 mx-auto">
        </a>
      </p>
      <p class="text-gray-700 mb-4">
        Eind maart 2025, als SVDJ het project open sourced, neemt Open State Foundation het beheer en de verdere ontwikkeling van Bron chat over.
      </p>
    </div>
    
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-xl font-semibold mb-2">Wat is het verdienmodel van Bron chat?</h2>
      <p class="text-gray-700 mb-4">
        Bron chat zal vanaf eind maart 2025 open source worden aangeboden aan de journalistieke sector.
        Vanaf dat moment wordt Bron chat gehost als gratis dienst van Open State Foundation, een onafhankelijke stichting zonder winstoogmerk.
        Hun missie: bijdragen aan een digitaal transparante overheid en daarmee aan een controleerbare en vitale democratie.
        Op de site van Open State Foundation vind je meer informatie over de financiële steun voor dit project (Bron chat) en de stichting.
      </p>
    </div>
    
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-xl font-semibold mb-2">Welke databronnen zitten er wel en niet in Bron chat?</h2>
      <p class="text-gray-700 mb-4">
        Bron chat is afhankelijk van documenten uit bronnen van Open State Foundation, de overheid en onderzoeksinstituten. 
        De compleetheid van deze bronnen is nooit volledig. Overheidsorganen waar we geen data van hebben zijn: gemeente Súdwest-Fryslân en provincies Flevoland en Groningen.
      </p>
      <p class="text-gray-700 mb-4">
        Er wordt op het moment een <a href="https://bron.live/data" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">Data Quality Reporting tool</a> ontwikkeld om visueel in kaart te brengen welke data wel en niet in Bron, en Bron chat zitten. 
        Deze zal binnenkort te vinden zijn op <a href="https://bron.live/data" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">https://bron.live/data</a>.
      </p>
      <ul class="list-disc text-gray-700 space-y-2 pl-8 mb-4 mb-4">
        <li>
          <strong>Openraadsinformatie:</strong> raadsstukken van honderden gemeenten. Hier mist wel een flink aantal overheden: 37 gemeenten, 5 provincies en 17 waterschappen hebben zich niet aangesloten. Voor de overheden die wel aangesloten zijn, halen we dagelijks nieuwe documenten binnen. Deze documenten halen we binnen via de aanbieders van de systemen die deze overheden daarvoor hebben ingehuurd. Het binnenhalen van deze documenten gaat soms mis omdat onze verzoeken worden geblokkeerd of documenten missen. Er wordt momenteel gewerkt aan een fix die bijna al deze gebreken moet oplossen. Voor meer informatie zie:
          <a href="https://openraadsinformatie.nl" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
            openraadsinformatie.nl
          </a>.
        </li>
        <li>
          <strong>PoliFLW:</strong> Nieuwsberichten van lokale politieke partijen. Deze worden van de websites van de partijen gedownload (ge-’scraped’). Het komt zo nu en dan voor dan een website wijzigt of tijdelijk offline gaat. Daardoor komen niet alle nieuwsberichten in de PoliFLW database. Zie
          <a href="https://poliflw.nl" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
            poliflw.nl
          </a>
        </li>
        <li>
          <strong>Lokale wet- en regelgeving:</strong> Wetten en regels van decentrale overheden zoals gemeenten, provincies en waterschappen.
          Zie:
          <a href="https://lokaleregelgeving.overheid.nl" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
            lokaleregelgeving.overheid.nl
          </a>
        </li>
        <li>
          <strong>Woo-verzoeken:</strong> Woo-verzoeken, besluiten en bijbehorende documenten uit de database van
          <a href="https://woogle.nl" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
            Woogle.nl
          </a>
        </li>
        <li>
          <strong>Officiële Bekendmakingen:</strong> de officiële publicaties van het Staatsblad, de Staatscourant, het Tractatenblad, de Gemeentebladen, Provinciale bladen,
          Waterschapsbladen en Bladen gemeenschappelijke regeling.
          Zie:
          <a href="https://www.officielebekendmakingen.nl/" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
            officielebekendmakingen.nl
          </a>
        </li>
        <li>
          <strong>Rapporten:</strong> Alle overheidsrapporten zoals adviezen, visie documenten, strategieën, monitoren, etc.
          Zie:
          <a
            href="https://open.overheid.nl/zoekresultaten"
            class="text-blue-600 hover:underline"
            target="_blank"
            rel="noopener noreferrer"
          >
            open.overheid.nl/zoekresultaten
          </a>
        </li>
      </ul>
      <p class="text-gray-700 mb-4">
        Bron chat is afhankelijk van documenten uit bronnen van Open State Foundation, de overheid en onderzoeksinstituten.
        De compleetheid van deze bronnen is nooit volledig.
        Wat zit niet in Bron chat? We zetten de belangrijkste voor je op een rij:
      </p>
      <ul class="list-disc text-gray-700 space-y-2 pl-8 mb-4">
        <li>
          <strong>Openraadsinformatie:</strong> hier mist een flink aantal overheden (46 gemeenten, 5 provincies en 17 waterschappen hebben zich niet aangesloten).
          Voor de overheden die wel aangesloten zijn, halen we dagelijks nieuwe documenten binnen.
          Deze documenten halen we binnen via de aanbieders van de systemen die deze overheden daarvoor hebben ingehuurd.
          Het binnenhalen van deze documenten gaat soms mis omdat onze verzoeken worden geblokkeerd of documenten missen.
          Er wordt momenteel gewerkt aan een fix die bijna al deze gebreken moet oplossen.
        </li>
        <li>
          <strong>PoliFLW:</strong> de nieuwsberichten van politieke partijen. Deze worden van de websites van de partijen gedownload (ge-‘scraped’).
          Het komt zo nu en dan voor dan een website wijzigt of tijdelijk offline gaat.
          Daardoor komen niet alle nieuwsberichten in de PoliFLW database.
        </li>
      </ul>
    </div>
  
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-xl font-semibold mb-2">Hoe actueel is de data in Bron chat?</h2>
      <p class="text-gray-700 mb-4">
        Open State Foundation brengt 3,5 miljoen documenten samen op één centrale plek.
        Het actualiseren, updaten en beter doorzoekbaar maken van al die informatie is een continu proces.
        Er zitten documenten in Bron chat tot en met 10 oktober 2024, mits het opgenomen is in
        <a href="https://openstate.eu/nl/projecten-tools-data/resultaten/bron/" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">Bron</a>
        (het platform van Open State Foundation waarin alle data bij elkaar wordt gebracht).
        Er wordt op het moment gewerkt aan een oplossing waarbij Bron chat dagelijks wordt geüpdatet met de laatste documenten.
      </p>
    </div>
  
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-xl font-semibold mb-2">Als Bron chat iets niet vindt, bestaat het dan ook niet?</h2>
      <p class="text-gray-700 mb-4">
        Het is mogelijk dat een document dat je zoekt, wel bestaat, maar niet gevonden wordt door Bron chat. Waar kan dat aan liggen?
        Om vast te stellen of de documenten die je zoekt mogelijk niet in de Bron database zijn opgenomen,
        kun je hier de data kwaliteitsrapportage lezen:
        <a href="https://bron.live/data" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
          https://bron.live/data
        </a>
      </p>
    </div>
  
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-xl font-semibold mb-2">
        Mijn zoekopdracht levert niet de documenten die ik zoek, terwijl deze wel in de Bron database moeten zitten. Kan ik die documenten alsnog vinden?
      </h2>
      <p class="text-gray-700 mb-4">
        Het is mogelijk dat de zoekopdracht die wordt gebruikt niet goed aansluit op de inhoud van het document dat wordt gezocht,
        of dat andere documenten als relevanter worden geacht, waardoor het gezochte document niet wordt gepresenteerd als resultaat.
        Wat kun je hier aan doen? Probeer de zoekopdracht anders te formuleren zodat het zo specifiek mogelijk aansluit
        bij de titel en inhoud van het document.
      </p>
    </div>
  
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-xl font-semibold mb-2">Waarom krijg ik soms verschillende documenten in de zoekresultaten met een identieke zoekopdracht?</h2>
      <p class="text-gray-700 mb-4">
        Bron chat gebruikt zogenaamde 'vector search' in combinatie met het traditionele zoekalgoritme (BM25) op basis van 'keywords'.
        In de vector search zit een bepaalde toevalligheid ingebakken. Dit is de kracht van de technologie,
        maar kan er ook voor zorgen dat je met twee identieke zoekopdrachten verschillende documenten te zien krijgt in de zoekresultaten.
      </p>
    </div>
  
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-xl font-semibold mb-2">Kan ik het antwoord van Bron chat wel vertrouwen?</h2>
      <p class="text-gray-700 mb-4">
        Ja, en nee. Het gegenereerde antwoord van Bron chat kan onjuistheden bevatten.
        Dit is helaas inherent aan de technologie (LLMs) die we nu gebruiken.
        De kracht van Bron chat is echter dat je altijd de bron documenten bij de hand hebt om te kunnen verifiëren of het gegenereerde antwoord wel klopt.
      </p>
      <p class="text-gray-700 mb-4">
        Je kunt het gegenereerde antwoord het beste zien als een betrouwbare samenvatting van een lijst van betrouwbare bronnen.
        Dankzij de ingebouwde citaten is het altijd mogelijk om de correctheid van het gegenereerde antwoord te verifiëren in de bron documenten.
        Het antwoord op de vraag wordt gegenereerd door een 'large language model'.
        Deze technologie is gebaseerd op een bepaalde toevalligheid.
        Dit is zowel de grootste kracht, als een potentiële zwakte.
      </p>
    </div>
  
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-xl font-semibold mb-2">Welke modellen worden gebruikt in Bron chat?</h2>
      <p class="text-gray-700 mb-4">
        Op het moment – in de prototype fase – worden modellen van
        <a href="https://cohere.com/" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
          Cohere
        </a>
        gebruikt. Specifiek zijn dit <em>command-r-08-2024</em>, <em>command-r</em>, en <em>rerank-v3.5</em>.
        Voor de embeddings wordt het <em>embed-multilingual-v3.0</em> model gebruikt.
      </p>
      <p class="text-gray-700 mb-4">
        Onze doelstelling is om in de toekomst open source modellen te gaan gebruiken.
        Wellicht het nieuwe
        <a href="https://gpt-nl.nl/" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
          GPT-NL
        </a>
        dat in Q4 van 2025 wordt verwacht, waar Open State Foundation ook aan meewerkt.
      </p>
    </div>
  
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-xl font-semibold mb-2">Hoe zit het met privacy en wat gebeurt er met mijn data?</h2>
      <p class="text-gray-700 mb-4">
        Bron chat slaat de zoekopdrachten op, en de feedback die wordt gegeven via de like/dislike knoppen.
        Bron chat bewaart niets over jouw identiteit als gebruiker.
        Deze data wordt momenteel in de cloud in Frankrijk opgeslagen bij OVH. Zie OVH privacy policy:
        <a href="https://www.ovhcloud.com/nl/personal-data-protection/" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
          https://www.ovhcloud.com/nl/personal-data-protection/
        </a>.        
      </p>
      <p class="text-gray-700 mb-4">
        De server wordt beheerd door onze developer Jeremy Crowlesmith. Zodra de SVDJ de code van het project open sourced, wordt het beheer van de server overgedragen aan de Open State Foundation.
      </p>
      <p class="text-gray-700 mb-4">
        De zoekopdrachten en chats die via de API van Cohere worden gegenereerd worden door dit bedrijf opgeslagen.
        Deze data mogen door Cohere niet gebruikt worden om modellen te trainen of te fine-tunen.
        Meer details hierover vind je hier:
        <a href="https://trustcenter.cohere.com/" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
          https://trustcenter.cohere.com/
        </a>
      </p>
      <p class="text-gray-700 mb-4">
        We verzamelen ook analytische gegevens over het gebruik van Bron chat via Plausible Analytics.
        Dit is een open-source project dat zorgvuldig en in overeenstemming met de GDPR met de data omgaat.
        Raadpleeg hier hun gegevensbeleid:
        <a href="https://plausible.io/data-policy" class="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
          https://plausible.io/data-policy
        </a>
      </p>
    </div>
  
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-xl font-semibold mb-2">Wat willen jullie bereiken met Bron chat?</h2>
      <p class="text-gray-700 mb-4">
        Bron chat democratiseert het doen van onderzoek, doordat zoeken in openbare overheidsdata (3,5 miljoen documenten,
        van bijvoorbeeld raadsvergaderingen gepubliceerde Woo verzoeken) nu flexibel en makkelijk wordt voor alle soorten journalisten en onderzoekers,
        zowel landelijk als in de regio. Hierdoor kan de journalistiek met minder middelen meer bereiken.
        Onze visie voor Bron chat, en diensten die er mogelijk in de toekomst nog bij gaan komen,
        is dat iedere journalist in Nederland moet kunnen onderzoeken op een hoog niveau.
      </p>
    </div>
  
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-xl font-semibold mb-2">Hoe zeker is het dat Bron chat blijft bestaan?</h2>
      <p class="text-gray-700 mb-4">
        Tot eind maart 2025 wordt Bron chat als prototype ondersteund door de SVDJ Incubator.
        Daarna wordt het overgenomen als een dienst van Open State Foundation, en daarmee afhankelijk van donaties.
        Ben je er net als wij van overtuigd dat iedereen vrij moet kunnen beschikken over vitale overheidsinformatie
        over bijvoorbeeld het onderwijs, de zorg of het klimaat?
        Steun dan Open State Foundation in haar missie voor digitale transparantie bij de overheid.
        <!-- <a
          href="https://openstate.eu/nl/doneren/"
          class="text-blue-600 hover:underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          Doneren kan via dit formulier
        </a>. -->
      </p>
    </div>
  
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-xl font-semibold mb-2">Waarom bestaat Bron chat?</h2>
      <p class="text-gray-700 mb-4">
        Sinds 2012 wordt overheidsheidsdata al ontsloten door Open State Foundation.
        Toch maken journalisten spaarzaam gebruik van de data in
        <a
          href="https://openstate.eu/nl/projecten-tools-data/resultaten/bron/"
          class="text-blue-600 hover:underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          Bron
        </a>.
        Hoge werkdruk in combinatie met steeds grotere datasets – denk aan Woo-verzoeken met tientallen en soms honderden documenten –
        werpen drempels op voor onderzoekende journalisten.
      </p>
    </div>
  
    <div class="bg-white rounded-lg p-2 shadow-sm">
      <h2 class="text-xl font-semibold mb-2">Toekomst: wat komt er nog aan?</h2>
      <p class="text-gray-700 mb-4">
        Het team achter Bron chat wil journalisten in het hele land gaan ondersteunen met diensten en tools
        om samen onderzoek te doen naar serieuze onderwerpen.
        Op termijn hopen we dat journalisten en ook betrokken burgers steeds meer gaan samenwerken op dossiers
        die zowel landelijk als lokaal spelen, zoals bijvoorbeeld PFAS of de situatie rond dijken en rivieren.
      </p>
    </div>
  
  </div>
  
</div> 