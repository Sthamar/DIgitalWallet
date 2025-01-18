<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    let categoryName = '';
    /**
     * @type {{ name: string; monthly_limit: number; } | null}
     */
    let categoryData = null;
    let errorMessage = '';
    let successMessage = '';
    let isLoading = false;

    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

    $: categoryName = $page.params.categoryName;

    async function fetchCategory() {
        const token = localStorage.getItem('token');
        if (!token) {
            errorMessage = 'User is not authenticated.';
            return;
        }

        try {
            const res = await fetch(`${apiBaseUrl}/budget-categories/${categoryName}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (res.ok) {
                categoryData = await res.json();
            } else {
                const error = await res.json();
                errorMessage = error.detail || 'Failed to fetch category.';
            }
        } catch (error) {
            console.error('Error fetching category:', error);
            errorMessage = 'An unexpected error occurred. Please try again.';
        }
    }

    // Handle category update
    async function updateCategory() {
        // @ts-ignore
        if (!categoryData.name.trim() || categoryData.monthly_limit <= 0) {
            errorMessage = 'Please provide a valid name and budget limit.';
            return;
        }

        const token = localStorage.getItem('token');
        if (!token) {
            errorMessage = 'User is not authenticated.';
            return;
        }

        isLoading = true;
        errorMessage = '';
        successMessage = '';

        try {
            const res = await fetch(`${apiBaseUrl}/budget-categories/update/${categoryName}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    // @ts-ignore
                    name: categoryData.name,
                    // @ts-ignore
                    monthly_limit: categoryData.monthly_limit,
                }),
            });

            if (res.ok) {
                successMessage = 'Category updated successfully!';
                // Optionally, redirect to the list of categories or another page
                goto('/budget');
            } else {
                const error = await res.json();
                errorMessage = error.detail || 'Failed to update category.';
            }
        } catch (error) {
            console.error('Error updating category:', error);
            errorMessage = 'An unexpected error occurred. Please try again.';
        } finally {
            isLoading = false;
        }
    }

    onMount(() => {
        fetchCategory();
    });
</script>

<div class="hero bg-base-200 min-h-screen">
    <div class="hero-content text-center">
        <div class="card bg-base-200 w-full max-w-md shrink-0 shadow-2xl">
            <h1 class="text-5xl font-bold">Edit Budget Category</h1>

            {#if errorMessage}
                <div class="text-error font-mono m-2 bg-base-200">{errorMessage}</div>
            {/if}

            {#if successMessage}
                <div class="text-success font-mono m-2 bg-base-200">{successMessage}</div>
            {/if}

            {#if !categoryData}
                <p>Loading...</p>
            {:else}
                <form class="card-body" on:submit|preventDefault={updateCategory}>
                    <div class="form-control mb-6">
                        <label class="label" for="name">
                            <span class="label-text">Name</span>
                        </label>
                        <input
                            type="text"
                            id="name"
                            class="input input-bordered"
                            bind:value={categoryData.name}
                        />
                    </div>

                    <div class="form-control mb-6">
                        <label class="label" for="budget_limit">
                            <span class="label-text">Budget Limit</span>
                        </label>
                        <input
                            type="number"
                            id="budget_limit"
                            class="input input-bordered"
                            bind:value={categoryData.monthly_limit}
                        />
                    </div>

                    <button class="btn btn-primary mb-6" type="submit" disabled={isLoading}>
                        {isLoading ? 'Updating...' : 'Update'}
                    </button>
                </form>
            {/if}
        </div>
    </div>
</div>
