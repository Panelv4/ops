async function loadDashboard(){

const res = await fetch("/api/dashboard");
const data = await res.json();

document.getElementById("employees").innerHTML=data.employees;
document.getElementById("customers").innerHTML=data.customers;
document.getElementById("orders").innerHTML=data.orders;
document.getElementById("revenue").innerHTML="₹"+data.revenue;

}

loadDashboard();
setInterval(loadDashboard,5000);
