let editingId = null;

async function loadEmployees(){

    const res = await fetch("/api/employees");
    const data = await res.json();

    const tbody = document.getElementById("empTable");
    tbody.innerHTML="";

    data.forEach(e=>{

        tbody.innerHTML += `
        <tr>
            <td>${e.id}</td>
            <td>${e.name||""}</td>
            <td>${e.email||""}</td>
            <td>${e.phone||""}</td>
            <td>${e.department||""}</td>
            <td>${e.position||""}</td>
            <td>${e.status||""}</td>
            <td>
                <button onclick='editEmployee(${JSON.stringify(e)})'>✏️</button>
                <button onclick='deleteEmployee(${e.id})'>🗑️</button>
            </td>
        </tr>`;
    });

}

async function loadStats(){

    const res=await fetch("/api/employees/stats");
    const s=await res.json();

    document.getElementById("statsBox").innerHTML=
    `
    <b>Total:</b> ${s.total}
    &nbsp;&nbsp;
    <b>Active:</b> ${s.active}
    &nbsp;&nbsp;
    <b>Inactive:</b> ${s.inactive}
    `;

}

function showAddModal(){

    editingId=null;

    modalTitle.innerText="Add Employee";

    name.value="";
    email.value="";
    phone.value="";
    dept.value="";
    position.value="";
    salary.value="";
    status.value="Active";

    modal.style.display="block";

}

function editEmployee(e){

    editingId=e.id;

    modalTitle.innerText="Edit Employee";

    name.value=e.name||"";
    email.value=e.email||"";
    phone.value=e.phone||"";
    dept.value=e.department||"";
    position.value=e.position||"";
    salary.value=e.salary||0;
    status.value=e.status||"Active";

    modal.style.display="block";

}

async function saveEmployee(){

    const payload={

        name:name.value,
        email:email.value,
        phone:phone.value,
        department:dept.value,
        position:position.value,
        salary:Number(salary.value)||0,
        status:status.value

    };

    const url=editingId
        ?"/api/employees/"+editingId
        :"/api/employees";

    const method=editingId?"PUT":"POST";

    await fetch(url,{
        method,
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(payload)
    });

    showToast("Employee saved successfully");
    closeModal();

    await loadEmployees();
    await loadStats();

}

async function deleteEmployee(id){

    if(!confirm("Delete employee?")) return;

    await fetch("/api/employees/"+id,{
        method:"DELETE"
    });

    loadEmployees();
    loadStats();

}

function closeModal(){

    modal.style.display="none";

}

loadEmployees();
loadStats();
