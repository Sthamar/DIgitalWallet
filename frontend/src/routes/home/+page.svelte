<script>
    import { onMount } from "svelte";
    
    import { username, apiBaseUrl, user_pin} from "../../stores/user";
    let errorMessage = "";

</script>

<div class="hero min-h-screen">
    <div class="hero-content text-center">
        <div>
            {#if username}
                <h1 class="text-5xl m-5">Hello, <strong>{$username}</strong></h1>
            {:else}
                <p>{errorMessage}</p>
            {/if}
            <h1 class="text-5xl font-bold m-5">Welcome to Your Digital Wallet</h1>
            <p class="m-5">Track your budgets and expenses with ease.</p>
        <div>
            <a href="/budget" class="btn btn-primary">View Budget Categories</a>
            {#if $user_pin === '' || $user_pin === null}
                <a href="/set-pin" class="btn btn-primary">Set PIN</a>
            {:else}
                <a href="/expense" class="btn btn-primary">Set Expenses</a>
                <a href="/wallet" class="btn btn-primary">Wallet</a>
            {/if}
            
        </div>
        </div>
    </div>
</div>

