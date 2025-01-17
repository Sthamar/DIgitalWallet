<script>
    import "tailwindcss/tailwind.css";
    import { page } from '$app/stores';
    let nav_list = [
        {"item":"Home","link":"/"},
        {"item":"Budget", "link":"/budget"},
        {"item":"Log Out", "link":"#", "onClick": handleLogout}
    ]

    function handleLogout(){
        localStorage.removeItem('token');
        window.location.href = "/login";
    }
</script>
{#if $page.url.pathname !== '/login' && $page.url.pathname !== '/registration'}
    

<div class="navbar bg-base-100">
    <div class="flex-1">
        <a href="/" class="btn btn-ghost text-xl">Paisa</a>
    </div>
    <div class="flex-none">
        <ul class="menu menu-horizontal px-1">
            {#each nav_list as nav }
                <li>
                    {#if nav.onClick}
                        <a href="#" on:click={nav.onClick}>{nav.item}</a>
                    {:else}
                        <a href={nav.link}>{nav.item}</a>
                    {/if}
                    
                </li>
            {/each}
            
        </ul>
    </div>

</div>
{/if}
<slot/>