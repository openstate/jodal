# Bron Chat

Bron Chat is een tool voor journalisten en onderzoekers. Onze missie: openbare overheidsinformatie makkelijk en snel doorzoekbaar maken door middel van een AI chat. Dagelijks werken wij aan het uitbreiden en verbeteren van Bron chat. De tool is op het moment in beta.

## Development

Deze code is ontwikkeld door [linksmith](https://github.com/linksmith), tijdens SVDJ Incubator 2024-2025 programma van de SVDJ in samenwerking met Open State Foundation.

## 🌟 Functies

- **AI-gestuurde inzichten**: Ontdek verbanden en patronen in overheidsdata
- **Uitgebreide documentendatabase**: Doorzoek 3,5 miljoen overheidsdocumenten op één centrale plek
- **Bronverwijzingen**: Directe links naar originele documenten en downloadbare pdf's
- **Samenwerking**: Deel je zoekresultaten eenvoudig met collega's via deelbare links
- **Transparante data**: Ontsloten door Open State Foundation, een onafhankelijke stichting zonder winstoogmerk
- **Speciaal voor journalisten**: Een betrouwbare, flexibele tool ontwikkeld door SVDJ Incubator

## 🚀 Projectstructuur

Het project bestaat uit twee hoofdcomponenten:

### Backend (FastAPI)

- Gebouwd met FastAPI, een modern Python webframework
- Integreert met LLM-diensten (Cohere en LiteLLM)
- Gebruikt Qdrant voor vector search
- MySQL-database voor het opslaan van sessies en berichten
- Implementeert streaming responses voor real-time chat

### Frontend (SvelteKit)

- Gebouwd met SvelteKit, een modern JavaScript framework
- Responsieve UI met Tailwind CSS
- Real-time chatinterface
- Documentweergave en deelmogelijkheden

## 🛠️ Technologiestack

### Backend
- Python 3.x
- FastAPI
- SQLAlchemy
- Qdrant (Vector Database)
- Cohere/LiteLLM (LLM Services)
- MySQL
- Alembic (Database Migrations)

### Frontend
- SvelteKit
- Tailwind CSS
- TypeScript/JavaScript
- Markdown-weergave

### Infrastructuur
- Docker & Docker Compose
- Traefik (Reverse Proxy)
- Sentry (Error Tracking)
- Phoenix (Observability)

## 🏗️ Ontwikkelingsomgeving

### Vereisten
- Docker en Docker Compose
- Node.js (voor frontend-ontwikkeling)
- Python 3.x (voor backend-ontwikkeling)

### Omgevingsvariabelen
Maak een `.env`-bestand aan in de hoofdmap met de volgende variabelen:

```
# Algemeen
ENVIRONMENT=development
PUBLIC_API_URL=http://localhost:8000/api

# Database
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=bron_chat
MYSQL_USER=bron_user
MYSQL_PASSWORD=your_password

# Qdrant
QDRANT_HOST=qdrant
QDRANT_PORT=6333

# LLM Services
COHERE_API_KEY=your_cohere_api_key
LLM_SERVICE=cohere  # of litellm

# Toegestane oorsprong
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8000
```

### De applicatie draaien

#### Ontwikkelingsmodus
```bash
# Start de applicatie in ontwikkelingsmodus met hot-reloading
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

#### Productiemodus
```bash
# Start de applicatie in productiemodus als achtergrondproces
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

#### Stagingmodus
```bash
# Start de applicatie in stagingmodus als achtergrondproces
docker-compose -f docker-compose.yml -f docker-compose.stag.yml up -d
```

## 📝 API-documentatie

Bij het draaien van de applicatie is de API-documentatie beschikbaar op:
- Ontwikkeling: http://localhost:8000/docs
- Productie/Staging: https://your-domain.com/docs

## 👥 Team

Bron Chat is ontwikkeld door een team van SVDJ Incubator dat bestaat uit:
- Jeremy Crowlesmith [linksmith](https://github.com/linksmith)
- Henri Bouwmeester
- Joost van de Loo

Het project maakt gebruik van de data van Bron, een product van Open State Foundation.

## 🔮 Toekomstvisie

Bron Chat democratiseert het doen van onderzoek, doordat zoeken in openbare overheidsdata nu flexibel en makkelijk wordt voor alle soorten journalisten en onderzoekers, zowel landelijk als in de regio. Hierdoor kan de journalistiek met minder middelen meer bereiken.

Onze visie voor Bron Chat, en diensten die er mogelijk in de toekomst nog bij gaan komen, is dat iedere journalist in Nederland moet kunnen onderzoeken op een hoog niveau.

## 📄 Licentie

Dit project is gelicenseerd onder de MIT-licentie:

```
MIT License

Copyright (c) 2025 Bron

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
``` 


---

## 🤝 SVDJ Incubator 2024-2025

Bron chat is tot stand gekomen tijdens de SVDJ Incubator 2024-2025. De SVDJ Incubator is een subsidie- en begeleidingsprogramma van het Stimuleringsfonds voor de Journalistiek (SVDJ) gericht op het vinden van oplossingen voor gedeelde vraagstukken binnen de journalistieke sector. 

Het SVDJ stimuleert met kennisdeling, begeleiding en subsidie een onafhankelijke, diverse en toekomstbestendige journalistieke infrastructuur in Nederland. 

Voor vragen over de SVDJ Incubator of de oplossingen die hieruit voort zijn gekomen, ga naar www.svdj.nl/incubator. 