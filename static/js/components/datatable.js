class DataTable{

constructor(tableId){

this.table=document.getElementById(tableId);

}

render(data){

if(!data.length){

this.table.innerHTML="<tr><td>No data found</td></tr>";

return;

}

const cols=Object.keys(data[0]);

let html="<thead><tr>";

cols.forEach(c=>{

html+="<th>"+c+"</th>";

});

html+="</tr></thead><tbody>";

data.forEach(r=>{

html+="<tr>";

cols.forEach(c=>{

html+="<td>"+(r[c]??"")+"</td>";

});

html+="</tr>";

});

html+="</tbody>";

this.table.innerHTML=html;

}

}
