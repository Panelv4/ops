
let revenueChart;


async function loadDashboardV2(){

try{


const summaryRes =
await fetch("/api/dashboard/summary");


const summary =
await summaryRes.json();



animateNumber(
"employeesCount",
summary.employees ?? 0
);


animateNumber(
"crmCount",
summary.crm ?? summary.customers ?? 0
);


animateNumber(
"inventoryCount",
summary.inventory ?? 0
);


document.getElementById("revenueCount").innerText =
"₹" + (summary.revenue ?? 0);



loadChart();



const activityRes =
await fetch("/api/dashboard/activity");


const activity =
await activityRes.json();



let html="";


if(Array.isArray(activity)){

activity.forEach(a=>{

html += `

<div class="activity-item">

✓ ${a.message ?? a.action ?? "System activity"}

</div>

`;

});


}


document.getElementById("activityFeed").innerHTML =
html || "No recent activity";updateInsights(summary);



}

catch(e){

console.log(e);

}

}




function animateNumber(id,value){

const el =
document.getElementById(id);


let start=0;


const speed =
Math.max(value/50,1);



const timer=setInterval(()=>{


start += speed;


if(start>=value){

start=value;

clearInterval(timer);

}


el.innerText =
Math.floor(start);


},20);


}





function loadChart(){


const ctx =
document.getElementById("revenueChart");


if(!ctx)return;



if(revenueChart){

revenueChart.destroy();

}



revenueChart =
new Chart(ctx,{

type:"line",

data:{


labels:[
"Jan",
"Feb",
"Mar",
"Apr",
"May",
"Jun"
],


datasets:[{

label:"Revenue",

data:[
12000,
18000,
15000,
24000,
28000,
35000
],

borderWidth:3,

tension:.4

}]

},


options:{


responsive:true,


plugins:{


legend:{


display:false

}

}

}

});


}



loadDashboardV2();


setInterval(
loadDashboardV2,
30000
);

function updateInsights(data){


let insights = [];


if((data.inventory ?? 0) < 10){

insights.push(
"⚠ Inventory levels need attention"
);

}
else{

insights.push(
"📦 Inventory is stable"
);

}



if((data.employees ?? 0) > 0){

insights.push(
"👥 Workforce is active"
);

}


insights.push(
"📈 Monitor revenue growth trends"
);



document.getElementById("insightsBox").innerHTML =

insights.map(i=>`

<div class="ai-insight">

${i}

</div>

`).join("");

}

