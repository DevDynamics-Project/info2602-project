async function getRoutine(){
    const response = await fetch('/api/workouts', {
  headers: {
    Authorization: `Bearer ${localStorage.getItem("token")}`
  }
});

    return response.json();
}
function loadRoutine(workouts){
    const container = document.querySelector('#routine-container');

    container.innerHTML = workouts.map(workout => `
        <div class="col-md-6 col-lg-4">
            <div class="card text-center p-3">

                <div style="height:120px;" class="mb-3"></div>

                <h5>${workout.name}</h5>
                <p>${workout.muscle} • ${workout.difficulty}</p>

                <button class="btn btn-dark" onclick="deleteWorkout(${workout.id})">
                    Delete
                </button>

            </div>
        </div>
    `).join("");
}

function deleteWorkout(id){
    alert("Removed from routine!");
}

async function main(){
    const routine = await getRoutine();
    loadRoutine(routine);
}

main();