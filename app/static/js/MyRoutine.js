async function getRoutine(){
    const response = await fetch('/api/routine');
    return response.json();
}

function loadRoutine(workouts){
    const container = document.querySelector('#routine-container');

    container.innerHTML = workouts.map(workout => `
        <div class="col-md-6 col-lg-4">
            <div class="card text-center p-3">

                <div style="height:120px; background:black;" class="mb-3"></div>

                <h5>${workout.name}</h5>
                <p>${workout.muscle} | ${workout.difficulty}</p>

                <button class="btn btn-dark" onclick="deleteWorkout(${workout.id})">
                    Delete
                </button>

            </div>
        </div>
    `).join("");
}

async function deleteWorkout(id){
    console.log("Delete workout:", id);

    // future API call
    /*
    await fetch(`/api/routine/${id}`, {
        method: 'DELETE'
    });
    */

    // refresh after delete
    main();
}

async function main(){
    const routine = await getRoutine();
    loadRoutine(routine);
}

main();