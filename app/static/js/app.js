async function getWorkoutData(){
    const response = await fetch('/api/workouts', {
        method: "GET",
        credentials: "include"
    });

    return response.json();
}

function loadWorkouts(workouts){
    const container = document.querySelector('#result');

    container.innerHTML = workouts.map(workout => `
        <div class="col-md-6 col-lg-4">
            <div class="card text-center p-3">

                <div style="height:120px;" class="mb-3"></div>

                <h5>${workout.name}</h5>
                <p>${workout.muscle} • ${workout.difficulty}</p>

                <button class="btn btn-dark" onclick="addToRoutine(${workout.id})">
                    Add
                </button>

            </div>
        </div>
    `).join("");
}

function addToRoutine(id){
    alert("Added to routine!");
}

async function main(){
    const workouts = await getWorkoutData();
    loadWorkouts(workouts);

    // search
    document.getElementById("search").addEventListener("input", (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = workouts.filter(w =>
            w.name.toLowerCase().includes(term)
        );
        loadWorkouts(filtered);
    });
}

main();