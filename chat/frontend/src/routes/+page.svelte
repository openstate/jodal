<script>
    import { goto } from '$app/navigation';
    import { API_BASE_URL } from '$lib/config';
    import ChatInput from '$lib/components/ChatInput.svelte';
    import Typed from 'typed.js';
    import { onMount, onDestroy } from 'svelte';
	import SearchInput from '../lib/components/SearchInput.svelte';
    import { base } from '$app/paths';

    let query = '';
    let isLoading = false;
    let error = null;

    const MAINTENANCE_MODE = false; // You can toggle this to enable/disable maintenance mode
    const MAINTENANCE_MESSAGE = "Bron chat is momenteel niet beschikbaar wegens onderhoud. Wanneer we weer online zijn wordt zoeken nog beter en gemakkelijker! Probeer het later opnieuw.";

    let samplePrompts = [
        {
            query: "Ravijnjaar 2026",
            text: "Ravijnjaar 2026"
        },
        {
            query: "Lerarentekort",
            text: "Lerarentekort in Utrecht",
            filters: {
                locations: [
                    {
                        "id": "GM0344",
                        "name": "Utrecht",
                        "type": "Gemeente"
                    }                    
                ],
            }
        },
        {
            query: "Woningvoorraad",
            text: "Woningvoorraad in Leeuwarden",
            filters: {
                locations: [   
                    {
                        "id": "GM0080",
                        "name": "Leeuwarden",
                        "type": "Gemeente"
                    },                 
                ],     
            }
        },
        {
            query: "Impact van AI op de arbeidsmarkt?",
            text: "Impact van AI op de arbeidsmarkt?",
        },
        {
            query: "Energietransitie", 
            text: "Energietransitie", 
        },
        {
            query: "Hoe beschermt de overheid tegen cyberdreigingen?",
            text: "Hoe beschermt de overheid tegen cyberdreigingen?",
        }
    ];
    
    let displayedPrompts = [];
    
    function getRandomPrompts() {
        let shuffled = [...samplePrompts].sort(() => 0.5 - Math.random());
        displayedPrompts = shuffled.slice(0, 2);
    }
    
    function handlePromptClick(prompt) {
        const urlSearchParams = new URLSearchParams({
            query: prompt.query.trim(),
            rewrite_query: 'true'
        });

        // Add year range filters if present
        if (prompt.filters?.yearRange?.length === 2) {
            urlSearchParams.append('start_date', `${prompt.filters.yearRange[0]}-01-01`);
            urlSearchParams.append('end_date', `${prompt.filters.yearRange[1]}-12-31`);
        }

        let locations = [];
        if (prompt.filters?.locations?.length > 0) {
            locations = prompt.filters.locations;
            prompt.filters.locations.forEach(loc => {
                urlSearchParams.append('locations', loc.id);
            });
        }

        handleSearch({ detail: { urlSearchParams, selectedLocations: locations } });
    }
    
    async function handleSearch(event) {        
        console.debug('page handleSearch', event);
        isLoading = true;
        error = null;

        try {
            // First create a new session
            const sessionResponse = await fetch(`${API_BASE_URL}/new_session`, {
                method: 'POST',
            });

            if (!sessionResponse.ok) {
                console.error('Failed to create new session', sessionResponse);
                throw new Error('Failed to create new session');
            }

            const sessionData = await sessionResponse.json();
            const sessionId = sessionData.id;

            // Navigate to the session page
            await goto(`/s/${sessionId}`);

            event.detail.urlSearchParams.append('session_id', sessionId);

            // Get the URLSearchParams from the event detail
            const urlSearchParams = event.detail.urlSearchParams;

            // Dispatch the event with the search parameters
            window.dispatchEvent(new CustomEvent('initialQuery', {
                detail: { 
                    urlSearchParams: urlSearchParams,
                    selectedLocations: event.detail.selectedLocations 
                }
            }));

        } catch (err) {
            console.error('Error:', err);
            isLoading = false;
            error = 'Er is een fout opgetreden bij het verwerken van uw vraag.';
        }
    }

    onMount(() => {
        const typedTitle = new Typed('#typed-title', {
            strings: ["Vraag alles over 3.5 miljoen open overheidsdocumenten"],
            typeSpeed: 50,
            showCursor: false,
        });

        getRandomPrompts();

        return () => {
            typedTitle.destroy();
        };
    });

    onDestroy(() => {
    });


    function handleClickOutside(event) {
        if (event.target === event.currentTarget) {
            closeModal();
        }
    }

    function closeModal() {
        showAboutDialog = false;
    }

</script>

<svelte:head>
    <title>Bron chat - Vraag alles over 3.5 miljoen open overheidsdocumenten</title>
</svelte:head>

<div class="min-h-screen flex flex-col items-center justify-center bg-gray-100">
    {#if MAINTENANCE_MODE}
        <div class="fixed inset-0 bg-gray-900 bg-opacity-90 z-50 flex items-center justify-center p-4">
            <div class="bg-white rounded-lg p-8 max-w-md text-center shadow-xl">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 mx-auto mb-4 text-gray-500">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M11.412 15.655 9.75 21.75l3.745-4.012M9.257 13.5H3.75l2.659-2.849m2.048-2.194L14.25 2.25 12 10.5h8.25l-4.707 5.043M8.457 8.457 3 3m5.457 5.457 7.086 7.086m0 0L21 21" />
                </svg>
                <h2 class="text-2xl font-bold mb-4">Onderhoud</h2>
                <p class="text-gray-600">{MAINTENANCE_MESSAGE}</p>
            </div>
        </div>
    {/if}

    <div class="w-full max-w-2xl text-center mb-4">
        <h1 class="text-xl sm:text-3xl font-bold mb-2 sm:mb-4">
            Welkom bij Bron chat            
        </h1>
        <h2 id="typed-title" class="text-gray-600 text-lg lg:text-xl"></h2>
    </div>

    <div class="w-full max-w-2xl">
        <SearchInput
            bind:value={query}
            {isLoading}
            on:submit={handleSearch}
        />
    </div>

    <div class="w-full max-w-2xl mt-5 flex flex-wrap gap-2 justify-center">
        {#each displayedPrompts as prompt}
            <button
                on:click={() => handlePromptClick(prompt)}
                class="text-sm text-gray-600 bg-gray-50 px-3 py-1.5 rounded-full border border-gray-300 hover:bg-gray-50 hover:border-gray-400 transition-colors"
            >
                {prompt.text}
            </button>
        {/each}
    </div>

    <div class="w-full max-w-2xl text-center mt-4 md:mt-6 flex items-cente justify-center flex-wrap flex-row">
        <a 
            href="{base}/over-bron-chat"
            class="m-2 text-sm font-normal text-blue-600 hover:underline cursor-pointer"
            data-sveltekit-reload
        >       
            Over Bron chat
        </a>
        <a
            href="{base}/faq"
            class="m-2 text-sm font-normal text-blue-600 hover:underline cursor-pointer"
            data-sveltekit-reload
        >
            FAQ
        </a>
    </div>

    {#if error}
        <div class="mt-4 text-red-500">
            {error}
        </div>
    {/if}

</div>
