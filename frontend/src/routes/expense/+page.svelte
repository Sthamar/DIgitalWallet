<script>
// @ts-nocheck

    import { onMount } from "svelte";
    import { apiBaseUrl, username, user_pin } from "../../stores/user";
    import { json } from "@sveltejs/kit";
    

    
    /**
     * @type {any[]}
     */
    let categories= [];
    let description = "";
    let send_amount = 0;
    let receiver_id = "";
    let pin = "";
    let amount = 0;
    let selected_category = null;
    let errorMessage = "";
    let walletNumber = "";
    let successMessage = "";
    let isVisible = false;

    async function getCategory() {
    
        const token = localStorage.getItem('token')
        try{
            const res = await fetch(`${apiBaseUrl}/budget-categories/categories/`,{
                method: 'GET',
                headers: {'Authorization': `Bearer ${token}`}
            })
            if(res.ok){
                const data = await res.json();
                categories = data;
                console.log(categories)

            }else{
                const error = await res.json();
                errorMessage = error.detail || "failed to fetch Categories"
            }
        }catch(error){
            console.error("An error occurs:", error );
        }
    
    }


    async function getWallet() {
        const token = localStorage.getItem('token');

        try{
            const res = await fetch(`${apiBaseUrl}/wallet`,{
                method:'GET',
                headers:{'Authorization':`Bearer ${token}`}
            })
            if(res.ok){
                const data = await res.json();
                amount = data.balance;
                walletNumber = data.id;
                console.log(data)
            }else{
                const error = await res.json();
                errorMessage = error.detail || "failed to load balance"
            }
        }catch(error){
            console.error("An error occure: ", error);
        }
    }
   

    async function sendMoney() {
        const transactionData = {
            receiver_wallet_id: parseInt(receiver_id), 
            amount: parseFloat(send_amount).toFixed(2),
            category_id: parseInt(selected_category), 
            description: description.trim(), 
            pin: pin.trim(),
        };

        if (!receiver_id || !send_amount || !selected_category || !pin) {
            errorMessage = "All fields are required.";
            return;
        }

        const token = localStorage.getItem('token');

        try{
            const res = await fetch(`${apiBaseUrl}/transactions/send-money`,{
                method:'POST',
                headers: {'Content-Type':'application/json', 'Authorization':`Bearer ${token}`},
                body: JSON.stringify(transactionData),
            });
            if(res.ok){
                successMessage = "Money transfered successfully.";
                receiver_id = "";
                send_amount = 0;
                description = "";
                pin = "";
                selected_category = null;
                getCategory();
            }else{
                errorMessage = "Failed to transfer money.";
            }
                
        }catch(error){
            console.error("An error occure: ", error);
        }
    }

    function toggleVisibility(){
        isVisible = !isVisible;
    }

    onMount( () =>{
        getCategory();
        getWallet();
    })

</script>

<div  class="text-center m-5">
    <h1 class="text-5xl font-bold">Expense & Transfer Center</h1>
</div>
<div class="grid grid-cols-2">
    <div class="grid grid-rows-2 bg-base-200">
        <div class="hero-content justify-center flex-col text-center items-center">
            
            {#if successMessage}
                <p class="text-success">{successMessage}</p>
            {/if}
            {#if errorMessage}
                <p class="text-error">{errorMessage}</p>
            {/if}
                <div class="bg-primary-content shadow-xl p-4">
                    <h1 class="text-5xl font-bold">Total Balance</h1>
                    <h2 class="font-semibold">Rs. {isVisible ? amount : "****"} </h2>
                    <h2>Wallet No: <strong>{isVisible ? walletNumber: "*****"}</strong></h2>
                    <button on:click={toggleVisibility} class="btn btn-ghost mt-2">
                        {#if isVisible}
                            <i class="fas fa-eye-slash"></i> <!-- Hide icon -->
                        {:else}
                            <i class="fas fa-eye"></i> <!-- Show icon -->
                        {/if}
                    </button>
                </div>
        </div>
        <div class="hero-content justify-center flex-col text-center items-center">
            <h1 class="text-5xl font-bold">Budget Remaining</h1>
            {#if successMessage}
                <p class="text-success">{successMessage}</p>
            {/if}
            {#if errorMessage}
                <p class="text-error">{errorMessage}</p>
            {/if}
                <table class="table bg-primary-content shadow-xl">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Remaining Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each categories as category }
                            {#if category.over_spend}
                                <tr class="table-row bg-error">
                                    <td>{category.name}</td>
                                    <td>Rs.{category.remaining_budget}</td>
                                </tr>
                            {:else}
                                <tr class="table-row">
                                    <td>{category.name}</td>
                                    <td>Rs. {category.remaining_budget}</td>
                                </tr>
                            {/if}
                        {/each}
                    </tbody>
                </table>
        </div>
    </div>
    <div class="hero bg-base-200">
        <div class="hero-content justify-center flex-col text-center items-center">
            <h1 class="text-5xl font-bold">Send Money</h1>
            {#if successMessage}
                <p class="text-success">{successMessage}</p>
            {/if}
            {#if errorMessage}
                <p class="text-error">{errorMessage}</p>
            {/if}
            <div class="card-body bg-base-300 shadow-xl">
                <div class="form-control">
                    <!-- svelte-ignore a11y_label_has_associated_control -->
                    <label class="label">Receiver ID</label>
                    <input type="number" class="input input-bordered" bind:value={receiver_id}>
                </div>
                <div class="form-control">
                    <!-- svelte-ignore a11y_label_has_associated_control -->
                    <label class="label">Amount</label>
                    <input type="number" class="input input-bordered" bind:value={send_amount}>
                </div>
                <div class="form-control">
                    <!-- svelte-ignore a11y_label_has_associated_control -->
                    <label class="label">Select Category</label>
                    <select name="" id="" class="select select-bordered" bind:value={selected_category}>
                        <option value="" disabled selected>Select a category</option>
                        {#each categories as category }
                            <option value={category.id}>{category.name}</option>
                        {/each}
                    </select>
                </div>
                <div class="form-control">
                    <!-- svelte-ignore a11y_label_has_associated_control -->
                    <label class="label">Description</label>
                    <!-- svelte-ignore element_invalid_self_closing_tag -->
                    <textarea class="textarea textarea-bordered" bind:value={description}/>
                </div>
                <div class="form-control">
                    <!-- svelte-ignore a11y_label_has_associated_control -->
                    <label class="label">PIN</label>
                    <input type="password" class="input input-bordered" bind:value={pin}>
                </div>
                <button class="btn btn-primary mt-4" on:click={sendMoney}>Send</button>
            </div>
        </div>
    </div>
    
</div>


