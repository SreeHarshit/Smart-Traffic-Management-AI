// ==============================
// Live Analytics Dashboard
// ==============================

// KPI Elements
const totalVehicles = document.getElementById("totalVehicles");
const violations = document.getElementById("violations");
const emergency = document.getElementById("emergency");

// -----------------------------
// Pie Chart
// -----------------------------

const pieChart = new Chart(
    document.getElementById("pieChart"),
    {
        type: "pie",
        data: {
            labels: ["Cars", "Bikes", "Buses", "Trucks"],
            datasets: [{
                data: [0, 0, 0, 0]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    }
);

// -----------------------------
// Bar Chart
// -----------------------------

const barChart = new Chart(
    document.getElementById("barChart"),
    {
        type: "bar",
        data: {
            labels: ["Cars", "Bikes", "Buses", "Trucks"],
            datasets: [{
                label: "Vehicle Count",
                data: [0, 0, 0, 0]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    }
);

// -----------------------------
// Line Chart
// -----------------------------

const lineChart = new Chart(
    document.getElementById("lineChart"),
    {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Vehicles",
                data: [],
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    }
);

// -----------------------------
// Fetch Live Stats
// -----------------------------

async function updateDashboard() {

    const response = await fetch("/stats");
    const data = await response.json();

    // KPI Cards
    totalVehicles.textContent = data.total;
    violations.textContent = data.violations;
    emergency.textContent = data.emergency;

    // Pie Chart
    pieChart.data.datasets[0].data = [
        data.cars,
        data.bikes,
        data.buses,
        data.trucks
    ];
    pieChart.update();

    // Bar Chart
    barChart.data.datasets[0].data = [
        data.cars,
        data.bikes,
        data.buses,
        data.trucks
    ];
    barChart.update();

    // Line Chart
    lineChart.data.labels = data.history.map((_, i) => i + 1);
    lineChart.data.datasets[0].data = data.history;
    lineChart.update();

}

// Initial Load
updateDashboard();

// Refresh Every Second
setInterval(updateDashboard, 1000);