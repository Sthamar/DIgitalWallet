<script>
    import { onMount } from "svelte";

    let username = "";
    let errorMessage = "";

    const apiBaseUrl = "http://127.0.0.1:8000";

    onMount(async () => {
        try {
            const res = await fetch(`${apiBaseUrl}/auth/me`,{
                method: "GET",
                headers:{
                    "Authorization": `Bearer ${localStorage.getItem("token")}`,
                },
            });
            if (res.ok){
                const data = await res.json();
                username = data.username;
            }else{
                errorMessage = "Failded to fetch user details.";
            }

        }catch (error){
            errorMessage = "An error occured while fetching user details.";
        }
    })
</script>

{#if username}
    <p>Hello, {username}</p>
{:else}
    <p>{errorMessage}</p>
{/if}
<h1>Welcome to Your Digital Wallet</h1>
<p>Track your budgets and expenses with ease.</p>
<a href="/budget">View Budget Categories</a>
<a href="/login">Logout</a>