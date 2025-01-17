<script>
    import { onMount } from 'svelte';

    let username = "";
    let password = "";
    let errorMessage = ""; // To display errors to the user
    const apiBaseUrl = "http://127.0.0.1:8000"; // Adjust based on your API endpoint

    async function handleLogin() {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    formData.append('grant_type', 'password');

    try {
        const res = await fetch(`${apiBaseUrl}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData,
        });

        if (res.ok) {
            const data = await res.json();
            localStorage.setItem('token', data.access_token); // Save token
            window.location.href = '/budget'; // Redirect on success
        } else {
            const error = await res.json();
            alert(error.detail || "Login failed");
        }
    } catch (error) {
        console.error("Error during login:", error);
        alert("An unexpected error occurred. Please try again.");
    }
}

    onMount(() => {
        // If the user is already logged in, redirect to the budget page
        const token = localStorage.getItem('token');
        if (token) {
            window.location.href = '/budget';
        }
    });
</script>

<div class="hero bg-base-200 min-h-screen">
    <div class="hero-content text-center ">
        <div class="max-w-md">
            <h1 class="text-5xl font-bold mb-6">Login</h1>
            {#if errorMessage}
                <div class="error">{errorMessage}</div>
            {/if}
            <div class="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
                <form on:submit|preventDefault={handleLogin} class="card-body">
                    <div class="form-control">
                        <label for="username" class="label">Username</label>
                        <input class="input input-bordered" id="username" type="text" placeholder="Enter your username" bind:value={username} required />
                    </div>
                    <div class="form-control">
                        <label for="password" class="label">Password</label>
                        <input class="input input-bordered" id="password" type="password" placeholder="Enter your password" bind:value={password} required  />
                    </div>
                    <button type="submit" class="btn btn-primary mt-6">Login</button>
                </form>
                <p class="m-4">Don't have an account? <a href="/registration" class="text-accent">Sign Up</a></p>
            </div>
            
        </div>
    </div>

        
        
</div>







