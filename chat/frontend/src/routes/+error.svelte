<script>
    import { page } from '$app/stores';
</script>



<div class="flex items-center justify-center h-screen bg-gray-100">
    <div class=" flex flex-col items-center">
        <h1 class="text-2xl font-semibold text-gray-700">{$page.status}</h1>
        <p class="text-gray-700">{$page.error.message}</p>
    </div>
</div>
