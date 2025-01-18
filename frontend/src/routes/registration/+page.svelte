<script>
    import { onMount } from "svelte";

    let full_name = "";
    let username = "";
    let email = "";
    let phone = "";
    let password = "";
    let confirm_password = "";
    let errorMessage = "";

    const apiBaseUrl = "http://127.0.0.1:8000";

    async function signupHandle() {
    if (password !== confirm_password) {
        errorMessage = "Passwords do not match!";
        return;
    }

    const userData = {
        username,
        full_name: full_name,
        email,
        phone,
        password,
        role: "user",
    };

    try {
        const res = await fetch(`${apiBaseUrl}/users`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(userData),
        });

        if (res.ok) {
            const data = await res.json();
            alert("User created successfully!");
            window.location.href = "/login";
        } else {
            // If the response is not OK, attempt to parse error message
            const error = await res.json();
            errorMessage = error.detail || "Signup failed";
        }
    } catch (error) {
        console.error("Error during signup:", error);
        errorMessage = "An unexpected error occurred. Please try again.";
    }
}
</script>


<div class="hero bg-base-200 min-h-screen">
    <div class="hero-content text-center ">
        <div class="max-w-md">
            <h1 class="text-5xl font-bold mb-6">Sign Up</h1>
            {#if errorMessage}
                <div class="error text-red-500">{errorMessage}</div>
            {/if}
            <div class="card bg-base-100 w-full max-w-md shrink-0 shadow-2xl">
                <form on:submit|preventDefault={signupHandle} class="card-body">
                    <div class="form-control">
                        <label for="username" class="label">Username</label>
                        <input class="input input-bordered" id="username" type="text" placeholder="Enter your username" bind:value={username} required />
                    </div>
                    <div class="form-control">
                        <label for="full_name" class="label">Full Name</label>
                        <input class="input input-bordered" id="full_name" type="text" placeholder="Enter your full name" bind:value={full_name} required />
                    </div>
                    <div class="form-control">
                        <label for="email" class="label">Email</label>
                        <input class="input input-bordered" id="email" type="email" placeholder="Enter your email" bind:value={email} required />
                    </div>
                    <div class="form-control">
                        <label for="phone" class="label">Phone</label>
                        <input class="input input-bordered" id="phone" type="text" placeholder="Enter your Phone number" bind:value={phone} required />
                    </div>
                    <div class="form-control">
                        <label for="password" class="label">Password</label>
                        <input class="input input-bordered" id="password" type="password" placeholder="Enter your password" bind:value={password} required  />
                    </div>
                    <div class="form-control">
                        <label for="confirm_password" class="label">Confirm Password</label>
                        <input class="input input-bordered" id="confirm_password" type="password" placeholder="Enter your password" bind:value={confirm_password} required  />
                    </div>
                    <button type="submit" class="btn btn-primary mt-6">Sign Up</button>
                </form>
                <p class="m-4">Already have an account? <a href="/login" class="text-accent">Log In</a></p>
            </div>
            
        </div>
    </div>

        
        
</div>