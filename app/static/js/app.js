let allWorkouts = [];
let allRoutines = [];

async function fetchJSON(url, opts = {}) {
  const res = await fetch(url, { credentials: 'include', ...opts });
  if (!res.ok) {
    if (res.status === 401) { window.location.href = '/login'; return null; }
    throw new Error(`HTTP ${res.status}`);
  }
  return res.json();
}

function difficultyBadge(d) {
  const cls = { Easy: 'badge-easy', Medium: 'badge-medium', Hard: 'badge-hard' };
  return `<span class="badge ${cls[d] || 'badge-medium'}">${d}</span>`;
}

function renderRoutineOptions() {
  if (!allRoutines.length) return `<option value="">No routines yet</option>`;
  return allRoutines
    .map(r => `<option value="${r.id}">${r.name}</option>`)
    .join('');
}

function renderWorkoutGrid(workouts) {
  const grid = document.getElementById('workout-grid');

  if (!workouts.length) {
    grid.innerHTML = `
      <div class="empty-state" style="grid-column:1/-1">
        <div class="big">NO RESULTS</div>
        <div>Try a different search term</div>
      </div>`;
    return;
  }

  grid.innerHTML = workouts.map(w => `
    <div class="w-card" id="wcard-${w.id}">
      <div class="w-card-header">
        <span class="w-card-name">${escHtml(w.name)}</span>
        ${difficultyBadge(w.difficulty)}
      </div>
      <div class="w-card-desc">${escHtml(w.description)}</div>
      <div class="w-card-meta">
        <span class="badge badge-muscle">${escHtml(w.muscle_group)}</span>
        <span class="meta-tag">${w.duration} min</span>
      </div>
      <div class="w-card-actions">
        <select id="sel-${w.id}">
          <option value="">Add to routine…</option>
          ${renderRoutineOptions()}
        </select>
        <button class="btn btn-primary btn-sm" onclick="addToRoutine(${w.id})">Add</button>
      </div>
    </div>
  `).join('');
}

function handleSearch() {
  const q = document.getElementById('search').value.toLowerCase().trim();
  if (!q) { renderWorkoutGrid(allWorkouts); return; }
  const filtered = allWorkouts.filter(w =>
    w.name.toLowerCase().includes(q) ||
    w.muscle_group.toLowerCase().includes(q) ||
    w.difficulty.toLowerCase().includes(q) ||
    w.description.toLowerCase().includes(q)
  );
  renderWorkoutGrid(filtered);
}

async function addToRoutine(workoutId) {
  const sel = document.getElementById('sel-' + workoutId);
  const routineId = parseInt(sel.value);
  if (!routineId) { showToast('Select a routine first', true); return; }

  const routine = allRoutines.find(r => r.id === routineId);
  const workout = allWorkouts.find(w => w.id === workoutId);

  try {
    const result = await fetchJSON(`/api/routines/${routineId}/workouts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ workout_id: workoutId, sets: 3, reps: 10, order: 0 })
    });
    if (result) {
      showToast(`"${workout.name}" added to "${routine.name}"`);
      sel.value = '';
      allRoutines = await fetchJSON('/api/routines') || allRoutines;
    }
  } catch (e) {
    showToast(e.message || 'Already in routine', true);
  }
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

async function main() {
  try {
    [allWorkouts, allRoutines] = await Promise.all([
      fetchJSON('/api/workouts'),
      fetchJSON('/api/routines')
    ]);
    allWorkouts = allWorkouts || [];
    allRoutines = allRoutines || [];
    renderWorkoutGrid(allWorkouts);
  } catch (e) {
    document.getElementById('workout-grid').innerHTML =
      `<div class="empty-state" style="grid-column:1/-1"><div class="big">ERROR</div><div>${e.message}</div></div>`;
  }
}

main();
