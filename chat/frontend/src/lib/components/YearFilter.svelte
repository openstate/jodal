<script>
    import noUiSlider from 'nouislider';
    import 'nouislider/dist/nouislider.css';
    import { createEventDispatcher, onMount } from 'svelte';

    const dispatch = createEventDispatcher();    

    export let yearRange = [];
    let minYear = 2010;
    let maxYear = parseInt(new Date().getFullYear());
    let slider;

    function formatYear(value) {
        return value.toString();
    }

    function handleYearChange(values) {
        yearRange = values.map(Number);
        dispatch('yearUpdate', yearRange);
    }

    function handleClose() {
        dispatch('close');
    }

    onMount(() => {
        if (yearRange.length === 0) {
            yearRange = [minYear, maxYear];
        } 

        // Initialize noUiSlider
        noUiSlider.create(slider, {
            start: yearRange,
            connect: true,
            range: {
                'min': minYear,
                'max': maxYear
            },
            step: 1,
            tooltips: true,
            format: {
                to: formatYear,
                from: value => parseInt(value)
            }
        });

        // Event listener for slider updates
        slider.noUiSlider.on('set', (values) => {
            handleYearChange(values);
        });
    });
</script>

<div class="bg-white rounded-lg shadow-lg p-4 w-[500px] max-w-[calc(100vw-2rem)]">
    <div class="flex justify-between items-center mb-4">
        <h3 class="text-sm font-medium text-gray-700">Jaren</h3>
        <button 
            on:click={handleClose}
            class="text-gray-400 hover:text-gray-600 transition-colors"
        >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
        </button>
    </div>
    <div class="px-2">
        <div id="year-slider" bind:this={slider}></div>
    </div>
</div>

<style lang="postcss">    
    :global(#year-slider) {
        @apply mt-14 mb-3 mx-3;
    }

    :global(.noUi-target) {
        @apply bg-gray-200;
    }

    :global(.noUi-connect) {
        @apply bg-blue-500;
    }

    :global(.noUi-handle) {
        @apply bg-white border-2 border-blue-500;
    }
</style> 