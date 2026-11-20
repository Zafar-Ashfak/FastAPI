"use strict";

// Change this if your FastAPI server runs somewhere else.
const API_BASE = "http://127.0.0.1:8000";

// Same scale as the API's `grade` computed field.
const GRADE_CUTOFFS = [[90, "A+"], [80, "A"], [70, "AB"], [60, "B"], [50, "BC"], [40, "C"]];
const gradeOf = (marks) => (GRADE_CUTOFFS.find(([cut]) => marks >= cut) || [0, "F"])[1];

const $ = (sel) => document.querySelector(sel);
const esc = (v) =>
  String(v ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const fmt = (n) => String(Math.round(Number(n) * 10) / 10);

const state = {
  students: [],
  query: "",
  course: "",
  sort: "name:asc",
  page: 1,
  limit: 10,
  editingId: null,
  deletingId: null,
};

/* ───────────── API ───────────── */

function errorText(data, res) {
  const detail = data && data.detail;
  if (Array.isArray(detail)) {
    // FastAPI 422: [{loc: [...], msg: "..."}]
    return detail
      .map((e) => `${e.loc[e.loc.length - 1]}: ${String(e.msg).replace("Value error, ", "")}`)
      .join("\n");
  }
  return detail || res.statusText || "Request failed";
}

async function api(method, path, body) {
  let res;
  try {
    res = await fetch(API_BASE + path, {
      method,
      headers: body ? { "Content-Type": "application/json" } : undefined,
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new Error(`Can't reach the API at ${API_BASE}. Check that uvicorn is running and CORS is enabled.`);
  }
  let data = null;
  try { data = await res.json(); } catch { /* empty body */ }
  if (!res.ok) throw new Error(errorText(data, res));
  return data;
}

async function loadStudents() {
  try {
    const data = await api("GET", "/students"); // { "S001": {...}, ... }
    state.students = Object.entries(data).map(([id, s]) => ({ id, ...s }));
    $("#banner").hidden = true;
  } catch (err) {
    showBanner(err.message);
  }
  render();
}

/* ───────────── View ───────────── */

function visibleStudents() {
  const q = state.query.trim().toLowerCase();
  let list = state.students.filter((s) => {
    if (state.course && s.course !== state.course) return false;
    if (!q) return true;
    return [s.name, s.email, s.id].some((v) => String(v).toLowerCase().includes(q));
  });

  const [key, dir] = state.sort.split(":");
  list = [...list].sort((a, b) => {
    const diff = typeof a[key] === "string" ? a[key].localeCompare(b[key]) : a[key] - b[key];
    return dir === "desc" ? -diff : diff;
  });
  return list;
}

function render() {
  const all = state.students;
  const avg = all.length ? all.reduce((sum, s) => sum + s.marks, 0) / all.length : 0;
  $("#summary").textContent = all.length
    ? `${all.length} student${all.length === 1 ? "" : "s"}, class average ${avg.toFixed(1)}`
    : "No students yet.";

  renderCourses();

  const list = visibleStudents();
  const pages = Math.max(1, Math.ceil(list.length / state.limit));
  state.page = Math.min(state.page, pages);
  const start = (state.page - 1) * state.limit;
  const slice = list.slice(start, start + state.limit);

  $("#rows").innerHTML = slice
    .map((s) => {
      const g = gradeOf(s.marks);
      const skills = (s.skills || []).map((k) => `<span class="tag">${esc(k)}</span>`).join("");
      return `<tr>
        <td class="id">${esc(s.id)}</td>
        <td>${esc(s.name)}<small>${esc(s.email)}</small></td>
        <td>${esc(s.course)}</td>
        <td class="num">${esc(s.roll)}</td>
        <td class="num">${esc(s.age)}</td>
        <td class="num">${fmt(s.marks)}</td>
        <td><span class="grade g-${g.replace("+", "p")}">${g}</span></td>
        <td class="skills">${skills}</td>
        <td class="actions">
          <button class="btn small" data-edit="${esc(s.id)}" type="button">Edit</button>
          <button class="btn small del" data-delete="${esc(s.id)}" type="button">Delete</button>
        </td>
      </tr>`;
    })
    .join("");

  $("#empty").hidden = slice.length > 0;
  $("#pageInfo").textContent = list.length
    ? `${start + 1} to ${start + slice.length} of ${list.length}`
    : "0 results";
  $("#prev").disabled = state.page <= 1;
  $("#next").disabled = state.page >= pages;
}

function renderCourses() {
  const courses = [...new Set(state.students.map((s) => s.course))].sort((a, b) => a.localeCompare(b));
  if (state.course && !courses.includes(state.course)) state.course = "";

  $("#courseFilter").innerHTML =
    `<option value="">All courses</option>` +
    courses.map((c) => `<option value="${esc(c)}"${c === state.course ? " selected" : ""}>${esc(c)}</option>`).join("");
  $("#courseList").innerHTML = courses.map((c) => `<option value="${esc(c)}">`).join("");
}

function showBanner(msg) {
  const el = $("#banner");
  el.textContent = msg;
  el.hidden = false;
}

let toastTimer;
function toast(msg) {
  const el = $("#toast");
  el.textContent = msg;
  el.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove("show"), 2600);
}

/* ───────────── Add / edit ───────────── */

const form = $("#studentForm");

function openForm(student) {
  state.editingId = student ? student.id : null;
  form.reset();
  $("#formError").hidden = true;
  $("#formTitle").textContent = student ? `Edit ${student.name}` : "Add student";

  form.elements.id.disabled = Boolean(student);
  if (student) {
    form.elements.id.value = student.id;
    form.elements.name.value = student.name;
    form.elements.email.value = student.email;
    form.elements.roll.value = student.roll;
    form.elements.course.value = student.course;
    form.elements.age.value = student.age;
    form.elements.marks.value = student.marks;
    form.elements.skills.value = (student.skills || []).join(", ");
  } else {
    const nums = state.students.map((s) => /^S(\d+)$/.exec(s.id)).filter(Boolean).map((m) => Number(m[1]));
    form.elements.id.value = "S" + String((nums.length ? Math.max(...nums) : 0) + 1).padStart(3, "0");
    const rolls = state.students.map((s) => Number(s.roll)).filter(Boolean);
    form.elements.roll.value = rolls.length ? Math.max(...rolls) + 1 : 101;
  }
  $("#formDialog").showModal();
  form.elements.name.focus();
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const f = form.elements;
  const body = {
    name: f.name.value.trim(),
    email: f.email.value.trim(),
    roll: Number(f.roll.value),
    age: Number(f.age.value),
    course: f.course.value.trim(),
    marks: Number(f.marks.value),
    skills: f.skills.value.split(",").map((s) => s.trim()).filter(Boolean),
  };

  const saveBtn = $("#saveForm");
  saveBtn.disabled = true;
  $("#formError").hidden = true;

  try {
    if (state.editingId) {
      await api("PUT", `/update/${encodeURIComponent(state.editingId)}`, body);
      toast(`Updated ${body.name}`);
    } else {
      await api("POST", "/create", { id: f.id.value.trim(), ...body });
      toast(`Added ${body.name}`);
    }
    $("#formDialog").close();
    await loadStudents();
  } catch (err) {
    const box = $("#formError");
    box.textContent = err.message;
    box.hidden = false;
  } finally {
    saveBtn.disabled = false;
  }
});

$("#cancelForm").addEventListener("click", () => $("#formDialog").close());

/* ───────────── Delete ───────────── */

function openDelete(student) {
  state.deletingId = student.id;
  $("#deleteText").textContent = `${student.name} (${student.id}) will be removed from the registry. This can't be undone.`;
  $("#deleteError").hidden = true;
  $("#deleteDialog").showModal();
}

$("#confirmDelete").addEventListener("click", async () => {
  const btn = $("#confirmDelete");
  btn.disabled = true;
  try {
    await api("DELETE", `/delete/${encodeURIComponent(state.deletingId)}`);
    $("#deleteDialog").close();
    toast("Student deleted");
    await loadStudents();
  } catch (err) {
    const box = $("#deleteError");
    box.textContent = err.message;
    box.hidden = false;
  } finally {
    btn.disabled = false;
  }
});

$("#cancelDelete").addEventListener("click", () => $("#deleteDialog").close());

/* ───────────── Wiring ───────────── */

$("#addBtn").addEventListener("click", () => openForm(null));

$("#rows").addEventListener("click", (e) => {
  const edit = e.target.closest("[data-edit]");
  const del = e.target.closest("[data-delete]");
  if (edit) openForm(state.students.find((s) => s.id === edit.dataset.edit));
  if (del) openDelete(state.students.find((s) => s.id === del.dataset.delete));
});

$("#search").addEventListener("input", (e) => { state.query = e.target.value; state.page = 1; render(); });
$("#courseFilter").addEventListener("change", (e) => { state.course = e.target.value; state.page = 1; render(); });
$("#sort").addEventListener("change", (e) => { state.sort = e.target.value; state.page = 1; render(); });
$("#pageSize").addEventListener("change", (e) => { state.limit = Number(e.target.value); state.page = 1; render(); });
$("#prev").addEventListener("click", () => { state.page -= 1; render(); });
$("#next").addEventListener("click", () => { state.page += 1; render(); });

loadStudents();