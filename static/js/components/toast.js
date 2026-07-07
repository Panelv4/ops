function toast(msg,type="success"){

let t=document.createElement("div");

t.className="toast "+type;

t.innerHTML=msg;

document.body.appendChild(t);

setTimeout(()=>{
t.classList.add("show");
},100);

setTimeout(()=>{
t.remove();
},3500);

}

function toggleProfileMenu(){
    const menu = document.getElementById("profileMenu");
    if(menu.style.display === "block"){
        menu.style.display = "none";
    }else{
        menu.style.display = "block";
    }
}

document.addEventListener("click", function(e){
    const profile = document.querySelector(".profile");
    if(profile && !profile.contains(e.target)){
        document.getElementById("profileMenu").style.display = "none";
    }
});
