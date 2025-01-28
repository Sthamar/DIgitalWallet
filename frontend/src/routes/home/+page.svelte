<script>
    import { onMount, onDestroy, setContext } from "svelte";
    import { username, apiBaseUrl, user_pin } from "../../stores/user";
    import Chart from "chart.js/auto";
    
    /**
     * @type {Chart<"bar", number[], string>}
     */
    let chart;
    let errorMessage = "";

    onMount(() => {
        // @ts-ignore
        const ctx = document.getElementById("incomeExpenseChart").getContext("2d");
        chart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: ['Income', "Expense"],
                datasets: [{
                    label: "Amount",
                    data: [0, 0],
                    backgroundColor: ["#4caf50", "#f44336"],
                }]
            },
            
            options: {
                responsive: true,
                plugins: {
                    legend: { display: true },
                },
            },
        });

        // Use the apiBaseUrl dynamically for WebSocket connection
        const token = localStorage.getItem("token");
        const socket = new WebSocket(`${apiBaseUrl}/ws/transactions?token=${token}`);
        console.log(socket)
        socket.onmessage = (event) => {
            console.log(event.data)
            try {
                console.log(event.data)
                const { income, expense } = JSON.parse(event.data);
                console.log("Income and Expense updated: ", income, expense);
                chart.data.datasets[0].data = [income, expense];
                chart.update();
            } catch (e) {
                console.error("Error parsing WebSocket data:", e);
                errorMessage = "Failed to update chart data.";
            }
        };

        socket.onopen = () => {
            console.log("WebSocket connection established.");
            socket.send("Hello server");
        };

        socket.onclose = () => {
            console.log("WebSocket connection closed.");
        };

        // Cleanup WebSocket on component destroy
        onDestroy(() => {
            if (socket) {
                socket.close();
                console.log("WebSocket connection closed.");
            }
        });
    });
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
            <p class="m-5 text-lg"><strong>Paisa</strong>: Your Money, Your Control, Your Way.</p>
            <p class="m-5">Track your budgets and expenses with ease.</p>
            <div>
                <a href="/budget" class="btn btn-primary">View Budget Categories</a>
                {#if $user_pin === '' || $user_pin === null}
                    <a href="/set-pin" class="btn btn-primary">Set PIN</a>
                {:else}
                    <a href="/expense" class="btn btn-primary">Set Expenses</a>
                    <a href="/wallet" class="btn btn-primary">Wallet</a>
                {/if}

                <canvas id="incomeExpenseChart" width="400" height="200"></canvas>
            </div>
        </div>
    </div>
</div>


