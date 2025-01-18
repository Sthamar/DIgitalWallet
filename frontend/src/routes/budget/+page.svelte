<script>
    import { onMount } from "svelte";
    import { goto } from '$app/navigation';
    let name = "";
    let budget_limit = 1;
    let message = "";
    let errorMessage = "";
    let isLoading = false;
    /**
     * @type {string | any[]}
     */
    let categories = [];

    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

    async function createBudget() {
        if (!name.trim() || budget_limit <= 0) {
            errorMessage = "Please provide a valid name and budget limit.";
            return;
        }
        const token = localStorage.getItem("token");
        if (!token) {
            errorMessage = "User is not authenticated.";
            return;
        }

        const budgetData = { name, monthly_limit: budget_limit };
        message = "";
        errorMessage = "";
        isLoading = true;

        try {
            const res = await fetch(`${apiBaseUrl}/budget-categories`, {
                method: "POST",
                headers: { "Content-Type": "application/json" , "Authorization": `Bearer ${token}`,},
                body: JSON.stringify(budgetData),
            });

            if (res.ok) {
                const data = await res.json();
                message = "Budget created successfully!";
                getBudget()
            } else {
                const error = await res.json();
                errorMessage = error.detail || "Budget creation failed.";
            }
        } catch (error) {
            console.error("Error during budget creation:", error);
            errorMessage = "An unexpected error occurred. Please try again.";
        } finally {
            isLoading = false;
        }
    }


    async function getBudget(){
        const token = localStorage.getItem("token");
        if(!token){
            errorMessage = "User is not authenticated";
            return;
        }

        try{
            const res = await fetch(`${apiBaseUrl}/budget-categories/categories`,{
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`,
                }
            });
            if(res.ok){
                categories = await res.json();
            }else{
                const error = await res.json();
                errorMessage = error.detail || "Failed to fetch categories";
            }
        }catch(error){
            console.error("Error during fetching categories: ",error);
            errorMessage = "An unexpected error occured please try again later";
        }finally{
            isLoading = false;
        }
    }


    // @ts-ignore
    async function deleteCategory(categoryName) {
            const token = localStorage.getItem("token");
            if(!token){
                errorMessage = "User is not authenticated.";
            }

            try{
                const res = await fetch(`${apiBaseUrl}/budget-categories/delete/${categoryName}`,{
                    method: "DELETE",
                    headers:{
                        "Authorization":`Bearer ${token}`,
                    },
                });

                if (res.ok){
                    message = `Category "${categoryName}" deleted successfully.`;

                    getBudget();
                }else{
                    const error = await res.json();
                    errorMessage = error.detail || "Failed to delete category,";
                }
            }catch(error){
                console.error("Error deleting category: ", error);
                errorMessage = "An unexpected error occured. Please try again.";
            }
    }

    onMount (() =>{
        getBudget();
    })
</script>

<div class="hero bg-base-200 min-h-screen">
    <div class="hero-content text-center">
        <div class="card bg-base-200 w-full max-w-md shrink-0 shadow-2xl">
            <h1 class="text-5xl font-bold">Create Budget Category</h1>

            {#if message}
                <div class="text-success">{message}</div>
            {/if}

            {#if errorMessage}
                <div class="text-error font-mono m-2 bg-base-200">{errorMessage}</div>
            {/if}

            <form class="card-body" on:submit|preventDefault={createBudget}>
                <div class="form-control mb-6">
                    <label class="label" for="name">
                        <span class="label-text">Name</span>
                    </label>
                    <input type="text" id="name" class="input input-bordered" bind:value={name}>
                </div>

                <div class="form-control mb-6">
                    <label class="label" for="budget_limit">
                        <span class="label-text">Budget Limit</span>
                    </label>
                    <input type="number" id="budget_limit" class="input input-bordered" bind:value={budget_limit}>
                </div>

                <button class="btn btn-primary mb-6" type="submit" disabled={isLoading}>
                    {isLoading ? "Creating..." : "Create"}
                </button>
            </form>
                    <div class="card bg-base-200 w-full max-w-2xl shadow-2xl">
                        <h1 class="text-2xl font-bold">Budget Categories</h1>
            
                        {#if isLoading}
                            <div>Loading categories...</div>
                        {:else if errorMessage}
                            <div class="text-error font-mono m-2 bg-base-200">{errorMessage}</div>
                        {:else if categories.length === 0}
                            <div>No categories found.</div>
                        {:else}
                            <ul>
                                {#each categories as category}
                                    <li class="bg-base-300 p-4 m-2 border-b flex justify-between">
                                        <div>
                                            <strong>{category.name}</strong> - Limit: {category.monthly_limit} - Remaining: {category.remaining_budget}
                                        </div>
                                        <button class="btn btn-error" on:click={()=> deleteCategory(category.name)}>
                                            Delete
                                        </button>
                                        <button
                                            class="btn btn-secondary"
                                            on:click={() => goto(`/budget/${category.name}`)}
                                        >
                                            Update
                                        </button>                                 
                                    </li>
                                {/each}
                            </ul>
                        {/if}
                    </div>
        </div>
    </div>
</div>


