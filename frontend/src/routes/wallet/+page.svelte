<script>
    import { error, json } from "@sveltejs/kit";
    import { username,apiBaseUrl } from "../../stores/user";
    import { onMount } from "svelte";
    

    let amount = "";
    let errorMessage = "";
    let successMessage = "";
    let user_amount = "";

    async function loadFund() {
        const token = localStorage.getItem('token');
        const amountData = {amount: parseFloat(amount)};

        if(!token){
            errorMessage = "User not authenticated.";
            return;
        }
        if (isNaN(amountData.amount) || amountData.amount <= 0) {
            errorMessage = "Amount must be a valid number greater than 0.";
            return;
        }


        try{
            const res = await fetch(`${apiBaseUrl}/wallet/add-funds`,{
                method: "POST",
                headers:{"Content-Type":"application/json", "Authorization":`Bearer ${token}`},
                body: JSON.stringify(amountData)
            });
            if(res.ok){
                const data = await res.json();
                successMessage = "fund loaded successfully."
                getFund();
            }else{
                errorMessage = "failed to load fund."
            };
        }catch(error){
            console.error("An error occur while loading fund: ", error);
            errorMessage = "An error occur while loading fund. Please try again later.";
        }
    }

    async function getFund() {
        const token = localStorage.getItem('token');
        if(!token){
            errorMessage = "User not authenticated.";
        }

        try{
            const res = await fetch(`${apiBaseUrl}/wallet`,{
                method: "GET",
                headers: {"Authorization":`Bearer ${token}`},
            })
            if(res.ok){
                const data = await res.json();
                console.log(data);
                user_amount = data.balance;
            }else{
                errorMessage = "An error occur loading fund.";
            }
        }catch(error){
            console.error("An error occur while fetching fund.", error);
        }
    }


    onMount(async () => {
        getFund()
    })

</script>

<div class="flex flex-col">
    <div class="hero">
        <div class="hero-content flex-col text-center">
            <div class="card bg-base-300 shrink-0 shadow-sm p-10">
                <h3 class="text-4xl font-bold">{$username.toUpperCase()}'s Wallet Amount</h3>
                <div class="card-body">
                    <p>Rs. {user_amount}</p>
                </div>
            </div>
        </div>
    </div>
    <div class="hero">
        <div class="hero-content flex-col text-center">
            <div class="card bg-base-200 shrink-0 shadow-sm p-10">
                <h3 class="text-4xl font-bold"> Load Money to {$username.toUpperCase()}'s Wallet </h3>
                {#if errorMessage}
                    <p class="text-error">{errorMessage}</p>
                {/if}
                {#if successMessage}
                    <p class="text-success">{successMessage}</p>
                {/if}
                <div class="card-body">
                    <input type="text" name="" id="" placeholder="Enter the amount." bind:value={amount} class="input input-bordered">
                    <button class="btn btn-primary" on:click={loadFund}>Load Fund</button>
                </div>
            </div>
        </div>
    </div>
    
</div>
