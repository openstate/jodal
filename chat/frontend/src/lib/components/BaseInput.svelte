<script>
    import { createEventDispatcher, onMount } from 'svelte';
    import { computePosition, flip, shift, offset } from '@floating-ui/dom';
    import { API_BASE_URL } from '$lib/config';
    import LocationFilter from './LocationFilter.svelte';
    import YearFilter from './YearFilter.svelte';
    
    export let isLoading = false;
    export let value = '';
    export let placeholder = 'Chat met Bron...';
    export let locations = [];
    export let initialLocations = [];
    export let initialYearRange = [];
    
    const dispatch = createEventDispatcher();
    
    let rewriteQuery = true;
    let selectedLocations = [];
    let selectedYearRange = [];
    let showLocationFilter = false;
    let showYearFilter = false;
    let locationButton;
    let yearButton;
    let locationPopup;
    let yearPopup;

    let popupsReady = {
        location: false,
        year: false
    };

    $: {
        if (initialLocations.length > 0 && selectedLocations && selectedLocations.length === 0) {
            selectedLocations = initialLocations;
        }
        if (initialYearRange.length > 0 && selectedYearRange && selectedYearRange.length === 0) {
            selectedYearRange = initialYearRange;
        }
    }

    function handleSubmit(event) {
        console.debug('base input handleSubmit', event, value, rewriteQuery, selectedLocations, selectedYearRange);
        
        if (event?.preventDefault) {
            event.preventDefault();
        }
        
        if (!value.trim()) return;
        
        const urlSearchParams = new URLSearchParams({
            query: value.trim(),
        });

        if (rewriteQuery) {
            urlSearchParams.append('rewrite_query', 'true');
        }

        if (selectedLocations.length > 0) {
            selectedLocations.forEach(loc => {
                if (loc && loc.id) {
                    urlSearchParams.append('locations', loc.id);
                }
            });
        }
       
        if (selectedYearRange && selectedYearRange.length > 0) {
            urlSearchParams.append('start_date', selectedYearRange[0].toString() + '-01-01');
            urlSearchParams.append('end_date', selectedYearRange[1].toString() + '-12-31');
        }

        dispatch('submit', {
            urlSearchParams,
            selectedLocations
        });
    }

    function handleStop() {
        dispatch('stop');
    }

    function handleLocationsUpdate(event) {
        selectedLocations = event.detail.detail;
    }

    function handleYearUpdate(event) {
        selectedYearRange = event.detail;
        console.debug('selectedYearRange', selectedYearRange);
        // dispatch('yearUpdate', yearRange);
    }

    async function updatePopupPosition(button, popup, placement = 'top-start') {
        if (!button || !popup) return;
        
        const searchPanel = button.closest('.search-panel');
        if (!searchPanel) return;
        
        const searchPanelRect = searchPanel.getBoundingClientRect();
        
        const { x, y } = await computePosition(button, popup, {
            placement: 'top-start',
            middleware: [
                offset({ mainAxis: 8 }),
                flip(),
                {
                    name: 'alignPanel',
                    fn: ({ x, y }) => {
                        return {
                            x: window.scrollX + searchPanelRect.left,
                            y: window.scrollY + searchPanelRect.top - popup.offsetHeight - 8
                        };
                    }
                }
            ],
        });

        Object.assign(popup.style, {
            left: `${x}px`,
            top: `${y}px`,
            position: 'fixed',
            zIndex: '50'
        });

        if (popup === locationPopup) {
            popupsReady.location = true;
        } else if (popup === yearPopup) {
            popupsReady.year = true;
        }
    }

    function toggleLocationFilter() {
        showLocationFilter = !showLocationFilter;
        showYearFilter = false;
        popupsReady.location = false;
        if (showLocationFilter) {
            setTimeout(() => updatePopupPosition(locationButton, locationPopup), 0);
        }
    }

    function toggleYearFilter() {
        showYearFilter = !showYearFilter;
        showLocationFilter = false;
        popupsReady.year = false;
        if (showYearFilter) {
            setTimeout(() => updatePopupPosition(yearButton, yearPopup), 0);
        }
    }

    function handleClickOutside(event) {
        if (!locationButton?.contains(event.target) && !locationPopup?.contains(event.target)) {
            showLocationFilter = false;
        }
        if (!yearButton?.contains(event.target) && !yearPopup?.contains(event.target)) {
            showYearFilter = false;
        }
    }

    async function fetchLocations() {
        try {
            const response = await fetch(`${API_BASE_URL}/locations`);
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.status}`);
            }
            locations = await response.json();
        } catch (error) {
            console.error('Error fetching locations:', error);
        }
    }

    function removeLocationFilter(locationToRemove) {
        selectedLocations = selectedLocations.filter(location => location.id !== locationToRemove.id);
        dispatch('locationsUpdate', selectedLocations);
    }

    function removeYearFilter() {
        selectedYearRange = [];
    }

    onMount(() => {
        document.addEventListener('click', handleClickOutside);

        if (locations.length === 0) {
            fetchLocations();
        }

        return () => document.removeEventListener('click', handleClickOutside);
    });
</script>

<form on:submit={handleSubmit} class="relative">
    <div class="search-panel rounded-lg border border-gray-300 overflow-hidden mx-4 sm:mx-0">
        <div class="p-3 pb-1">
            <div class="">
                <textarea
                    bind:value
                    {placeholder}
                    class="w-full text-base p-2 bg-gray-100 rounded text-gray-900 focus:outline-none focus:ring-0"
                    autofocus
                    rows="1"
                    disabled={isLoading}
                    on:keydown={e => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            handleSubmit(e);
                        }
                        if (e.key === 'Escape' && isLoading) {
                            e.preventDefault();
                            handleStop();
                        }
                    }}
                ></textarea>
            </div>

            <div class="flex justify-between items-center">
                <!-- Filter Buttons -->
                <div class="flex space-x-2">
                    <button
                        bind:this={locationButton}
                        class="flex items-center space-x-1 px-0.5 text-sm text-gray-500 hover:text-gray-700 rounded-md hover:bg-gray-100"
                        on:click={toggleLocationFilter}
                        type="button"
                    >
                        {#if selectedLocations.length > 0}
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
                                <path fill-rule="evenodd" d="m11.54 22.351.07.04.028.016a.76.76 0 0 0 .723 0l.028-.015.071-.041a16.975 16.975 0 0 0 1.144-.742 19.58 19.58 0 0 0 2.683-2.282c1.944-1.99 3.963-4.98 3.963-8.827a8.25 8.25 0 0 0-16.5 0c0 3.846 2.02 6.837 3.963 8.827a19.58 19.58 0 0 0 2.682 2.282 16.975 16.975 0 0 0 1.145.742ZM12 13.5a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" clip-rule="evenodd" />
                            </svg>  
                        {:else}   
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5" >
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                            </svg>                     
                        {/if}
                        <span class="sr-only">Locatie</span>
                    </button>

                    <button
                        bind:this={yearButton}
                        class="flex items-center space-x-1 px-0.5 text-sm text-gray-500 hover:text-gray-700 rounded-md hover:bg-gray-100"
                        on:click={toggleYearFilter}
                        type="button"
                    >
                        {#if selectedYearRange.length > 0}
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
                                <path d="M12.75 12.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM7.5 15.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM8.25 17.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM9.75 15.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM10.5 17.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM12 15.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM12.75 17.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM14.25 15.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM15 17.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM16.5 15.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM15 12.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM16.5 13.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z" />
                                <path fill-rule="evenodd" d="M6.75 2.25A.75.75 0 0 1 7.5 3v1.5h9V3A.75.75 0 0 1 18 3v1.5h.75a3 3 0 0 1 3 3v11.25a3 3 0 0 1-3 3H5.25a3 3 0 0 1-3-3V7.5a3 3 0 0 1 3-3H6V3a.75.75 0 0 1 .75-.75Zm13.5 9a1.5 1.5 0 0 0-1.5-1.5H5.25a1.5 1.5 0 0 0-1.5 1.5v7.5a1.5 1.5 0 0 0 1.5 1.5h13.5a1.5 1.5 0 0 0 1.5-1.5v-7.5Z" clip-rule="evenodd" />
                            </svg>             
                        {:else}   
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5" >
                                <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5m-9-6h.008v.008H12v-.008ZM12 15h.008v.008H12V15Zm0 2.25h.008v.008H12v-.008ZM9.75 15h.008v.008H9.75V15Zm0 2.25h.008v.008H9.75v-.008ZM7.5 15h.008v.008H7.5V15Zm0 2.25h.008v.008H7.5v-.008Zm6.75-4.5h.008v.008h-.008v-.008Zm0 2.25h.008v.008h-.008V15Zm0 2.25h.008v.008h-.008v-.008Zm2.25-4.5h.008v.008H16.5v-.008Zm0 2.25h.008v.008H16.5V15Z" />
                            </svg>       
                        {/if}
                        <span class="sr-only">Jaar</span>
                    </button>

                    <div class="pl-2 flex items-center space-x-1 text-sm text-gray-400">
                        {#if selectedLocations.length === 0 && selectedYearRange.length === 0 }
                            <span>Filter op gemeente, provincie, ministerie of jaar</span> 
                        {:else}
                            {#if selectedLocations.length > 0}
                                <span>in</span>
                                {#if selectedLocations.length === 1}
                                    <span class="flex items-center">
                                        <button class="text-gray-500 cursor-pointer" type="button" on:click={e => { e.stopPropagation(); toggleLocationFilter(); }}>
                                            {selectedLocations[0].name}
                                        </button>
                                        <button class="cursor-pointer -mt-2" type="button" on:click={() => removeLocationFilter(selectedLocations[0])}>
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 h-3">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                                            </svg>
                                        </button>
                                    </span>
                                {:else if selectedLocations.length === 2}
                                    <span class="flex items-center">
                                        <button class="text-gray-500 cursor-pointer" type="button" on:click={e => { e.stopPropagation(); toggleLocationFilter(); }}>
                                            {selectedLocations[0].name}
                                        </button>
                                        <button class="cursor-pointer -mt-2" type="button" on:click={() => removeLocationFilter(selectedLocations[0])}>
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 h-3">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                                            </svg>
                                        </button>
                                    </span>

                                    <span> of </span>
                                    <span class="flex items-center">
                                        <button class="text-gray-500 cursor-pointer" type="button"  on:click={e => { e.stopPropagation(); toggleLocationFilter(); }}>
                                            {selectedLocations[1].name}
                                        </button>
                                        <button class="cursor-pointer -mt-2" type="button" on:click={() => removeLocationFilter(selectedLocations[1])}>
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 h-3">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                                            </svg>
                                        </button>
                                    </span>
                                {:else}
                                    {#each selectedLocations.slice(0, -1) as location}
                                        <span class="flex items-center">    
                                            <button class="text-gray-500 cursor-pointer" type="button"  on:click={e => { e.stopPropagation(); toggleLocationFilter(); }}>
                                                {location.name}
                                            </button>
                                            <button class="cursor-pointer -mt-2" type="button" on:click={() => removeLocationFilter(location)}>
                                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 h-3">
                                                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                                                </svg>
                                            </button>,
                                        </span>
                                    {/each}
                                    <span> of </span>
                                    <span class="flex items-center">
                                        <button class="text-gray-500 cursor-pointer" type="button"  on:click={e => { e.stopPropagation(); toggleLocationFilter(); }}>
                                            {selectedLocations[selectedLocations.length - 1].name}
                                        </button>
                                        <button class="cursor-pointer -mt-2" type="button" on:click={() => removeLocationFilter(selectedLocations[selectedLocations.length - 1])}>
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 h-3">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                                            </svg>
                                        </button>
                                    </span>
                                {/if}
                            {/if}

                            {#if selectedYearRange.length > 0 }
                                <span>
                                    tussen 
                                    <button class="text-gray-500 cursor-pointer" type="button" on:click={e => { e.stopPropagation(); toggleYearFilter(); }}>
                                        {selectedYearRange[0]}
                                    </button>
                                     en 
                                    <span class="inline-flex items-center">
                                        <button class="text-gray-500 cursor-pointer" type="button"  on:click={e => { e.stopPropagation(); toggleYearFilter(); }}>
                                            {selectedYearRange[1]}
                                        </button>
                                        <button class="cursor-pointer -mt-3" type="button" on:click={() => removeYearFilter()}>
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-3 h-3">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                                            </svg>
                                        </button>
                                    </span>
                                </span>
                            {/if}
                        {/if}
                    </div>
                </div>
                
                <!-- Search Button -->
                <div>
                    <slot name="button" {isLoading} {handleSubmit} {handleStop}></slot>
                </div>
            </div>
        </div>
    </div>

    {#if showLocationFilter}
        <div 
            bind:this={locationPopup} 
            class="fixed" 
            class:invisible={!popupsReady.location}
        >
            <LocationFilter
                bind:selectedLocations
                locations={locations}
                on:locationsUpdate={handleLocationsUpdate}
                on:close={() => showLocationFilter = false}
            />
        </div>
    {/if}

    {#if showYearFilter}
        <div 
            bind:this={yearPopup} 
            class="fixed"
            class:invisible={!popupsReady.year}
        >
            <YearFilter
                yearRange={selectedYearRange}
                on:yearUpdate={handleYearUpdate}
                on:close={() => showYearFilter = false}
            />
        </div>
    {/if}
</form> 