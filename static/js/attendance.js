async function loadAttendance() {
    let res = await fetch("/api/attendance");
    let data = await res.json();

    let tbody = document.getElementById("attTable");
    tbody.innerHTML = "";

    data.forEach(a => {
        tbody.innerHTML += `
        <tr>
            <td>${a.id}</td>
            <td>${a.employee_id}</td>
            <td>${a.check_in || "-"}</td>
            <td>${a.check_out || "-"}</td>
            <td>${a.work_hours || 0}</td>
        </tr>`;
    });
}

async function checkIn() {
    await fetch("/api/attendance/checkin", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            employee_id: 1,
            company_id: 1
        })
    });

    loadAttendance();
}

async function checkOut() {
    // simple version: updates latest record
    let res = await fetch("/api/attendance");
    let data = await res.json();

    if (data.length === 0) return;

    let latest = data[0];

    await fetch("/api/attendance/checkout/" + latest.id, {
        method: "POST"
    });

    loadAttendance();
}

loadAttendance();
