<script>
    import "tailwindcss/tailwind.css";
    import { page } from '$app/stores';
    import { onMount } from "svelte";
    import { username, apiBaseUrl, user_pin } from "../stores/user";


    let nav_list_1 = [
        {"item":"Home","link":"/home"},
        {"item":"Budget", "link":"/budget"},
        {"item":"Expense", "link":"/expense"},
        {"item":"Wallet", "link":"/wallet"},
        {"item":"Log Out", "link":"#", "onClick": handleLogout}
    ]

    let nav_list_2 = [
        {"item":"Home","link":"/home"},
        {"item":"Budget", "link":"/budget"},
        {"item":"Set Pin", "link":"/set-pin"},
        {"item":"Log Out", "link":"#", "onClick": handleLogout}
    ]
    let errorMessage ="";



    function handleLogout(){
        localStorage.removeItem('token');
        window.location.href = "/login";
    }

    async function getUsername() {
        const token = localStorage.getItem('token');

        try{
            const res = await fetch(`${apiBaseUrl}/auth/me`,{
                method:'GET',
                headers: {'Authorization':`Bearer ${token}`}
            })
            if (res.ok){
                const data = await res.json()
                username.set(data.username);

            }else{
                errorMessage = "failed to fetch user details.";
            }

        }catch(error){
            errorMessage ="An error occur while fetching user details.";
            console.error("error fetching data: ", error);
        }
    }

    async function getPin() {
        const token = localStorage.getItem('token');

        if(!token){
            errorMessage = "User not authenitcate."
        }

        try{
            const res = await fetch(`${apiBaseUrl}/users/pin`,{
                method: "GET",
                headers: {"Authorization":`Bearer ${token}`},
            })
            if(res.ok){
                const data = await res.json();
                user_pin.set(data.pin || null);
            }else{
                const error = await res.json();
                errorMessage = error.detail || "Failed to fetch pin"
            }
        }catch(error){
            console.error("An error occur: ", error);
            errorMessage = "An error occur. Please try again later.";
        }
    }


    onMount(async () => {
        getUsername(),
        getPin()
    })
    
</script>
{#if $page.url.pathname !== '/login' && $page.url.pathname !== '/registration'}
    

<div class="navbar bg-base-100">
    <div class="flex-1">
        <a href="/home" class="btn btn-ghost text-xl">Paisa</a>
    </div>
    <div class="flex-none">
        <ul class="menu menu-horizontal px-1">
            {#if $user_pin === null || $user_pin === ""}
                {#each nav_list_2 as nav }
                    <li>
                        {#if nav.onClick}
                            <a href="#" on:click={nav.onClick}>{nav.item}</a>
                        {:else}
                            <a href={nav.link}>{nav.item}</a>
                        {/if}
                        
                    </li>
                {/each}
            {:else}
                {#each nav_list_1 as nav }
                    <li>
                        {#if nav.onClick}
                            <a href="#" on:click={nav.onClick}>{nav.item}</a>
                        {:else}
                            <a href={nav.link}>{nav.item}</a>
                        {/if}
                        
                    </li>
                {/each}
            {/if}
            
            
        </ul>
    </div>

</div>
{/if}
<slot/>