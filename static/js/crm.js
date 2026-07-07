async function loadCRM() {
    const res = await fetch("/api/leads");
    const data = await res.json();

    const table = document.getElementById("crmTable");
    table.innerHTML = "";

    data.forEach(l => {
        table.innerHTML += `
        <tr>
            <td>${l.id}</td>
            <td>${l.name}</td>
            <td>${l.score}</td>
            <td>${l.status}</td>
        </tr>`;
    });
}

loadCRM();
