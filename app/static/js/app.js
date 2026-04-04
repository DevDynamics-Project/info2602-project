async function getWorkoutData(){
    const response = await fetch('/api/workouts'); // future endpoint
    return response.json();
}

function loadWorkouts(workouts){
    const container = document.querySelector('#result');

    container.innerHTML = workouts.map(workout => `
        <div class="col-md-6 col-lg-4">
            <div class="card text-center p-3">
                <div style="height:120px; background:black;" class="mb-3"></div>
                <h5>${workout.name}</h5>
                <p>${workout.muscle} | ${workout.difficulty}</p>
                <button class="btn btn-dark" onclick="addToRoutine(${workout.id})">
                    Add to Routine
                </button>
            </div>
        </div>
    `).join("");
}

function addToRoutine(id){
    console.log("Add workout:", id);

    // future API call example:
    /*
    fetch('/api/routine', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ workout_id: id })
    });
    */
}

async function main(){
    const workouts = await getWorkoutData();
    loadWorkouts(workouts);
}

main();