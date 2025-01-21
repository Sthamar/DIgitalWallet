<script>
    import { json } from "@sveltejs/kit";
    import { username, apiBaseUrl, user_pin } from "../../stores/user";
    
    
    let errorMessage = "";
    let pinset = "";
    let successMessage = "";

    async function setPin(){
        const token = localStorage.getItem('token');
        const pinData = {pin : pinset};
        if(!token){
            errorMessage = "User not authentcated."
        }
        
        try{
            const res = await fetch(`${apiBaseUrl}/users/me/set-pin`,{
                method: "POST",
                headers:{"Content-Type":"application/json", "Authorization":`Bearer ${token}`},
                body: JSON.stringify(pinData),
            });
            if(res.ok){
                const data = await res.json();
                successMessage = "PIN set successfully.";
                user_pin.set(pinset)
            }else{
                errorMessage = "Error to set PIN.";
            }
        }catch(error){
            console.error("An error occur: ", error);
            errorMessage = "An error occur. Please try again later.";
        }

    }
    
    


    

</script>

<div class="hero min-h-screen">
    <div class="hero-content bg-base-200 max-w-md text-center">
        <div class="card w-full max-w-md shrink-0 shadow-2xl">
            <div class="card-body">
                {#if $user_pin === '' || $user_pin === null} 
                    <h1 class="text-5xl font-bold">Set PIN</h1>
                    <input type="text" class="input input-bordered" placeholder="Enter PIN" bind:value={pinset}>
                    <button class="btn btn-primary" on:click={setPin}>Set Pin</button>
                {:else}
                    <p class="text-success bg-base-100 p-4">
                        <span class="font-bold">{$username.toUpperCase()}</span> has already set PIN
                    </p>
                    <a href="/home" class="btn btn-primary">Return to Home</a>
                {/if}

                {#if errorMessage}
                    <p class="text-red-500">{errorMessage}</p>
                {/if}

                {#if successMessage}
                    <p class="text-green-500">{successMessage}</p>
                {/if}
            </div>
        </div>
    </div>
</div>
