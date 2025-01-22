<script>
// @ts-nocheck

    import { error, json } from "@sveltejs/kit";
    import { username,apiBaseUrl } from "../../stores/user";
    import { onMount } from "svelte";
    

    let amount = "";
    let walletNumber = "";
    let errorMessage = "";
    let successMessage = "";
    let user_amount = "";
    /**
     * @type {any[]}
     */
    let transactions = [];
    /**
     * @type {any[]}
     */
    let received_transactions = [];
    /**
     * @type {any[]}
     */
    let send_transactions = [];
    let isVisible = false;

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
                sendTransactions();
                creditDebitTransactions();
                receivedTransactions();
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
                walletNumber = data.id;
            }else{
                errorMessage = "An error occur loading fund.";
            }
        }catch(error){
            console.error("An error occur while fetching fund.", error);
        }
    }

    async function creditDebitTransactions() {
        const token = localStorage.getItem('token');
        

        try{
            const res = await fetch(`${apiBaseUrl}/transactions/transactions/debit-credit`,{
                method:"GET",
                headers:{"Authorization":`Bearer ${token}`},
            })
            if(res.ok){
                const data = await res.json();
                transactions = data;
                console.log(transactions)

            }else{
                const error = await res.json();
                errorMessage = error.detail || "failed to fetch transaction data";
            }
        }catch(error){
            console.error("An error occure: ", error);
        }
    }

    async function sendTransactions() {
        const token = localStorage.getItem('token');
        

        try{
            const res = await fetch(`${apiBaseUrl}/transactions/transactions/send`,{
                method:"GET",
                headers:{"Authorization":`Bearer ${token}`},
            })
            if(res.ok){
                const data = await res.json();
                send_transactions = data;

            }else{
                const error = await res.json();
                errorMessage = error.detail || "failed to fetch transaction data";
            }
        }catch(error){
            console.error("An error occure: ", error);
        }
    }

    async function receivedTransactions() {
        const token = localStorage.getItem('token');
        

        try{
            const res = await fetch(`${apiBaseUrl}/transactions/transactions/received`,{
                method:"GET",
                headers:{"Authorization":`Bearer ${token}`},
            })
            if(res.ok){
                const data = await res.json();
                received_transactions = data;

            }else{
                const error = await res.json();
                errorMessage = error.detail || "failed to fetch transaction data";
            }
        }catch(error){
            console.error("An error occure: ", error);
        }
    }

    function toggleVisibility(){
        isVisible = !isVisible;
    }

    onMount(async () => {
        getFund();
        creditDebitTransactions();
        receivedTransactions();
        sendTransactions();
    })

</script>

<div class="text-center m-5">
    <h1 class="text-5xl font-bold">Wallet & Statements</h1>
</div>

<div class="grid grid-cols-2 gap-4 bg-base-100">
    <section class="car bg-base-200 shadow-xl m-4">
        <div class="hero">
            <div class="hero-content flex-col text-center">
                <div class="card bg-base-300 shrink-0 shadow-xl p-10">
                    <div class="bg-primary-content shadow-xl p-4">
                        <h1 class="text-5xl font-bold">Total Balance</h1>
                        <h2 class="font-semibold">Rs. {isVisible ? user_amount : "****"} </h2>
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
            </div>
        </div>
        <div class="hero">
            <div class="hero-content flex-col text-center">
                <div class="card bg-base-300 shrink-0 shadow-xl p-10">
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
        
    </section>
    <section class="card bg-base-200 shadow-xl m-4 text-center item-center grid grid-rows-2">
        <h1 class="text-5xl font-bold">Statements</h1>
        {#if transactions.length !== 0}
        <h1 class="text-2xl font-semibold m-4">Credit-Debit</h1>
        <div class="card overflow-y-auto" style="max-height: 200px;">
            
            <table class="table table-zebra bg-base-300 shadow-xl">
                <thead class="bg-slate-200">
                    <tr class="table-row">
                        <th>S.N</th>
                        <th>Amount</th>
                        <th>Description</th>
                        <th>Type</th>
                        <th>Date</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    {#each transactions as transaction, index }
                        <tr>
                            <td> {index + 1}</td>
                            <td>Rs. {transaction.amount}</td>
                            <td>{transaction.description}</td>
                            <td>{transaction.transaction_type}</td>
                            <td>{new Date(transaction.transaction_date).toLocaleDateString('en-CA')}</td>
                            <td>{new Date(transaction.transaction_date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true })}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
        {/if}
        
        {#if send_transactions.length !== 0}
        <h1 class="text-2xl font-semibold m-4">Send</h1>
        <div class="card overflow-y-auto" style="max-height: 200px;">
            <table class="table table-zebra bg-base-300 shadow-xl">
                <thead class="bg-slate-200">
                    <tr class="table-row">
                        <th>S.N</th>
                        <th>Amount</th>
                        <th>Description</th>
                        <th>Type</th>
                        <th>Date</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    {#each send_transactions.sort((a, b) => new Date(b.transaction_date) - new Date(a.transaction_date)) as transaction, index}
                        <tr>
                            <td>{index + 1}</td>
                            <td>Rs. {transaction.amount}</td>
                            <td>{transaction.description}</td>
                            <td>{transaction.transaction_type}</td>
                            <td>{new Date(transaction.transaction_date).toLocaleDateString('en-CA')}</td>
                            <td>{new Date(transaction.transaction_date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true })}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
    
    {#if received_transactions.length !== 0}
        <h1 class="text-2xl font-semibold m-4">Received</h1>
        <div class="card overflow-y-auto" style="max-height: 200px;">
            <table class="table table-zebra bg-base-300 shadow-xl">
                <thead class="bg-slate-200">
                    <tr class="table-row">
                        <th>S.N</th>
                        <th>Amount</th>
                        <th>Description</th>
                        <th>Type</th>
                        <th>Date</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    {#each received_transactions.sort((a, b) => new Date(b.transaction_date) - new Date(a.transaction_date)) as transaction, index}
                        <tr>
                            <td>{index + 1}</td>
                            <td>Rs. {transaction.amount}</td>
                            <td>{transaction.description}</td>
                            <td>{transaction.transaction_type}</td>
                            <td>{new Date(transaction.transaction_date).toLocaleDateString('en-CA')}</td>
                            <td>{new Date(transaction.transaction_date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true })}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
    
        
    </section>
</div>


