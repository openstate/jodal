<script>
    export let min;
    export let max;
    export let values = [min, max];
    
    let rangeWidth;
    let isDragging = false;
    let activeThumb = null;
    let container;
    
    $: leftPercent = ((values[0] - min) / (max - min)) * 100;
    $: rightPercent = ((values[1] - min) / (max - min)) * 100;
    
    function handleMouseDown(event, thumb) {
        isDragging = true;
        activeThumb = thumb;
        window.addEventListener('mousemove', handleMouseMove);
        window.addEventListener('mouseup', handleMouseUp);
    }
    
    function handleMouseMove(event) {
        if (!isDragging || !container) return;
        
        const rect = container.getBoundingClientRect();
        const percent = Math.min(Math.max(0, (event.clientX - rect.left) / rect.width), 1);
        const value = Math.round(min + percent * (max - min));
        
        if (activeThumb === 'left') {
            values[0] = Math.min(value, values[1]);
        } else {
            values[1] = Math.max(value, values[0]);
        }
        values = values; // trigger reactivity
    }
    
    function handleMouseUp() {
        isDragging = false;
        activeThumb = null;
        window.removeEventListener('mousemove', handleMouseMove);
        window.removeEventListener('mouseup', handleMouseUp);
    }
</script>

<div 
    class="relative h-2 bg-gray-200 rounded-full cursor-pointer"
    bind:this={container}
>
    <!-- Range track -->
    <div
        class="absolute h-full bg-blue-600 rounded-full"
        style="left: {leftPercent}%; right: {100 - rightPercent}%"
    ></div>
    
    <!-- Left thumb -->
    <div
        class="absolute w-4 h-4 bg-white border-2 border-blue-600 rounded-full -mt-1 -ml-2 cursor-grab"
        style="left: {leftPercent}%"
        on:mousedown={(e) => handleMouseDown(e, 'left')}
    ></div>
    
    <!-- Right thumb -->
    <div
        class="absolute w-4 h-4 bg-white border-2 border-blue-600 rounded-full -mt-1 -ml-2 cursor-grab"
        style="left: {rightPercent}%"
        on:mousedown={(e) => handleMouseDown(e, 'right')}
    ></div>
</div>

<style>
    /* Prevent text selection while dragging */
    div {
        user-select: none;
    }
</style> 