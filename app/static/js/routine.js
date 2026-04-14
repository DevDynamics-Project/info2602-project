let allWorkouts = [];
let allRoutines = [];
let remixState  = {};

async function fetchJSON(url, opts = {}) {
  const res = await fetch(url, { credentials: 'include', ...opts });
  if (!res.ok) {
    if (res.status === 401) { window.location.href = '/login'; return null; }
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `HTTP ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function difficultyBadge(d) {
  const cls = { Easy: 'badge-easy', Medium: 'badge-medium', Hard: 'badge-hard' };
  return `<span class="badge ${cls[d] || 'badge-medium'}" style="font-size:10px;padding:2px 7px">${d}</span>`;
}

function renderStats() {
  const totalEx   = allRoutines.reduce((s, r) => s + r.workouts.length, 0);
  const totalMins = allRoutines.reduce((s, r) =>
    s + r.workouts.reduce((ss, rw) => ss + (rw.workout.duration * rw.sets), 0), 0);
  document.getElementById('stats-grid').innerHTML = `
    <div class="stat-card"><div class="stat-label">Routines</div><div class="stat-val">${allRoutines.length}</div></div>
    <div class="stat-card"><div class="stat-label">Total exercises</div><div class="stat-val">${totalEx}</div></div>
    <div class="stat-card"><div class="stat-label">Est. minutes</div><div class="stat-val">${totalMins}</div><div class="stat-sub">sets × duration</div></div>
    <div class="stat-card"><div class="stat-label">Workouts in DB</div><div class="stat-val">${allWorkouts.length}</div></div>
  `;
}

// list r
function renderRoutineList() {
  const el = document.getElementById('routine-list');
  renderStats();

  if (!allRoutines.length) {
    el.innerHTML = `
      <div class="empty-state">
        <div class="big">NO ROUTINES YET</div>
        <div>Create your first routine above to get started</div>
      </div>`;
    return;
  }

  el.innerHTML = allRoutines.map(r => renderRoutineCard(r)).join('');

  allRoutines.forEach(r => {
    if (sessionStorage.getItem('open-' + r.id) === '1') {
      const card = document.getElementById('rc-' + r.id);
      if (card) card.classList.add('open');
    }
  });
}

function renderRoutineCard(r) {
  const totalMins = r.workouts.reduce((s, rw) => s + rw.workout.duration * rw.sets, 0);
  const exerciseRows = r.workouts.length
    ? r.workouts.slice().sort((a, b) => a.order - b.order).map(rw => renderExerciseRow(r.id, rw)).join('')
    : `<div style="padding:14px 0;color:var(--muted);font-size:13px">No exercises yet — add one below.</div>`;

  const available = allWorkouts.filter(w => !r.workouts.find(rw => rw.workout.id === w.id));

  return `
  <div class="routine-card" id="rc-${r.id}">
    <div class="routine-card-head" onclick="toggleRoutine(${r.id})">
      <div style="flex:1;min-width:0">
        <div class="routine-name">${escHtml(r.name)}</div>
        <div class="routine-meta">
          ${r.workouts.length} exercise${r.workouts.length !== 1 ? 's' : ''}
          &nbsp;·&nbsp; ~${totalMins} min
          ${r.description ? '&nbsp;·&nbsp; ' + escHtml(r.description) : ''}
        </div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;flex-shrink:0">
        <button class="btn btn-danger btn-sm" onclick="event.stopPropagation();deleteRoutine(${r.id})">Delete</button>
        <span class="routine-chevron">›</span>
      </div>
    </div>
    <div class="routine-card-body" id="rb-${r.id}">
      ${exerciseRows}
      <div class="add-exercise-row">
        <select id="add-sel-${r.id}">
          <option value="">Add exercise…</option>
          ${available.map(w => `<option value="${w.id}">${escHtml(w.name)} (${escHtml(w.muscle_group)})</option>`).join('')}
        </select>
        <button class="btn btn-outline btn-sm" onclick="addExercise(${r.id})">+ Add</button>
      </div>
    </div>
  </div>`;
}

function renderExerciseRow(routineId, rw) {
  const w   = rw.workout;
  const key = `${routineId}-${w.id}`;
  return `
  <div class="exercise-row" id="er-${key}">
    <div class="ex-info">
      <div class="ex-name">${escHtml(w.name)}</div>
      <div class="ex-sub">${escHtml(w.muscle_group)} · ${difficultyBadge(w.difficulty)} · ${w.duration} min</div>
    </div>
    <div class="ex-reps">
      <input class="reps-input" type="number" min="1" max="99" value="${rw.sets}"
        onchange="updateExercise(${routineId}, ${w.id}, {sets: parseInt(this.value)})">
      <span class="reps-label">sets</span>
      <input class="reps-input" type="number" min="1" max="99" value="${rw.reps}"
        onchange="updateExercise(${routineId}, ${w.id}, {reps: parseInt(this.value)})">
      <span class="reps-label">reps</span>
    </div>
    <div class="ex-actions">
      <button class="btn btn-remix btn-sm" onclick="toggleRemix(${routineId}, ${w.id})">Remix</button>
      <button class="btn btn-danger btn-sm" onclick="removeExercise(${routineId}, ${w.id})">×</button>
    </div>
  </div>
  <div class="remix-panel" id="rp-${key}" style="display:none">
    <h4>ALTERNATIVES FOR ${escHtml(w.name.toUpperCase())}</h4>
    <div class="alt-grid" id="ag-${key}"></div>
    <div style="margin-top:12px;display:flex;gap:8px">
      <button class="btn btn-remix btn-sm" onclick="applyRemix(${routineId}, ${w.id})">Apply Remix</button>
      <button class="btn btn-outline btn-sm" onclick="closeRemix(${routineId}, ${w.id})">Cancel</button>
    </div>
  </div>`;
}

function toggleRoutine(rid) {
  const card = document.getElementById('rc-' + rid);
  card.classList.toggle('open');
  sessionStorage.setItem('open-' + rid, card.classList.contains('open') ? '1' : '0');
}

// make rotine
async function createRoutine() {
  const name = document.getElementById('routine-name').value.trim();
  if (!name) { showToast('Enter a routine name', true); return; }
  const desc = document.getElementById('routine-desc').value.trim();
  try {
    const result = await fetchJSON('/api/routines', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description: desc })
    });
    if (result) {
      document.getElementById('routine-name').value = '';
      document.getElementById('routine-desc').value = '';
      showToast(`Routine "${name}" created!`);
      await refreshRoutines();
      sessionStorage.setItem('open-' + result.id, '1');
      renderRoutineList();
    }
  } catch (e) {
    showToast(e.message, true);
  }
}

// del routine
async function deleteRoutine(rid) {
  if (!confirm('Delete this routine?')) return;
  try {
    await fetchJSON(`/api/routines/${rid}`, { method: 'DELETE' });
    showToast('Routine deleted');
    await refreshRoutines();
  } catch (e) {
    showToast(e.message, true);
  }
}

// create exercise
async function addExercise(routineId) {
  const sel = document.getElementById('add-sel-' + routineId);
  const workoutId = parseInt(sel.value);
  if (!workoutId) return;
  try {
    await fetchJSON(`/api/routines/${routineId}/workouts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ workout_id: workoutId, sets: 3, reps: 10, order: 0 })
    });
    showToast('Exercise added!');
    sessionStorage.setItem('open-' + routineId, '1');
    await refreshRoutines();
  } catch (e) {
    showToast(e.message, true);
  }
}

// del exercise 
async function removeExercise(routineId, workoutId) {
  try {
    await fetchJSON(`/api/routines/${routineId}/workouts/${workoutId}`, { method: 'DELETE' });
    showToast('Exercise removed');
    sessionStorage.setItem('open-' + routineId, '1');
    await refreshRoutines();
  } catch (e) {
    showToast(e.message, true);
  }
}

async function updateExercise(routineId, workoutId, payload) {
  try {
    await fetchJSON(`/api/routines/${routineId}/workouts/${workoutId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  } catch (e) {
    showToast(e.message, true);
  }
}

async function toggleRemix(routineId, workoutId) {
  const key   = `${routineId}-${workoutId}`;
  const panel = document.getElementById('rp-' + key);
  const isOpen = panel.style.display === 'block';

  document.querySelectorAll('.remix-panel').forEach(p => { p.style.display = 'none'; });
  if (isOpen) return;

  const agEl = document.getElementById('ag-' + key);
  agEl.innerHTML = '<div style="color:var(--muted);font-size:13px">Loading alternatives…</div>';
  panel.style.display = 'block';

  try {
    const alts = await fetchJSON(`/api/routines/${routineId}/workouts/${workoutId}/alternatives`);
    remixState[key] = null;

    if (!alts || !alts.length) {
      agEl.innerHTML = '<div style="color:var(--muted);font-size:13px">No alternatives found with the same muscle group or difficulty.</div>';
      return;
    }

    agEl.innerHTML = alts.map(a => `
      <div class="alt-card" id="ac-${key}-${a.id}" onclick="pickAlt('${key}', ${a.id})">
        <div class="alt-card-name">${escHtml(a.name)}</div>
        <div class="alt-card-meta">${escHtml(a.muscle_group)} · ${difficultyBadge(a.difficulty)}</div>
        <div class="alt-card-meta" style="margin-top:4px">${a.duration} min · ${escHtml(a.description)}</div>
      </div>
    `).join('');
  } catch (e) {
    agEl.innerHTML = `<div style="color:var(--danger);font-size:13px">${e.message}</div>`;
  }
}

function pickAlt(key, altId) {
  remixState[key] = altId;
  document.querySelectorAll(`[id^="ac-${key}-"]`).forEach(el => el.classList.remove('picked'));
  document.getElementById(`ac-${key}-${altId}`).classList.add('picked');
}

async function applyRemix(routineId, workoutId) {
  const key   = `${routineId}-${workoutId}`;
  const newId = remixState[key];
  if (!newId) { showToast('Pick an alternative first', true); return; }

  try {
    await fetchJSON(`/api/routines/${routineId}/workouts/${workoutId}/remix`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ new_workout_id: newId })
    });
    const newName = allWorkouts.find(w => w.id === newId)?.name || 'new exercise';
    showToast(`Remixed to: ${newName}`);
    sessionStorage.setItem('open-' + routineId, '1');
    await refreshRoutines();
  } catch (e) {
    showToast(e.message, true);
  }
}

function closeRemix(routineId, workoutId) {
  document.getElementById(`rp-${routineId}-${workoutId}`).style.display = 'none';
}

async function refreshRoutines() {
  allRoutines = await fetchJSON('/api/routines') || [];
  renderRoutineList();
}

async function main() {
  try {
    [allWorkouts, allRoutines] = await Promise.all([
      fetchJSON('/api/workouts'),
      fetchJSON('/api/routines')
    ]);
    allWorkouts = allWorkouts || [];
    allRoutines = allRoutines || [];
    renderRoutineList();
  } catch (e) {
    document.getElementById('routine-list').innerHTML =
      `<div class="empty-state"><div class="big">ERROR</div><div>${e.message}</div></div>`;
  }
}

main();
