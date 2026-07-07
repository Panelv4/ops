cat > static/js/api.js << 'EOF'
const API = {

async get(url){
    const r = await fetch(url);
    return await r.js    const r = await fetch(url,{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(data)
    });
    return await r.json();
},

async put(url,data){
    const r = await fetch(url,{
        method:"PUT",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(data)
    });
    return await r.json();
},

async del(url){
    const r = await fetch(url,{
        method:"DELETE"
    });
    return await r.json();
}

};
