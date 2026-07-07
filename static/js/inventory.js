async function loadInventory() {

    const res = await fetch("/api/inventory");
    const data = await res.json();

    const table = document.getElementById("inventoryTable");
    table.innerHTML = "";

    let lowStock = 0;

    data.forEach(p => {

        if (p.quantity <= p.reorder_level) lowStock++;

        table.innerHTML += `
        <tr>
            <td>${p.id}</td>
            <td>${p.name}</td>
            <td>${p.category || ""}</td>
            <td>${p.quantity}</td>
            <td>${p.buying_price}</td>
            <td>${p.selling_price}</td>
            <td>${p.quantity <= p.reorder_level ? "⚠ Low" : "OK"}</td>
        </tr>`;
    });

    document.getElementById("inventoryStats").innerHTML = `
        <b>Total Items:</b> ${data.length}
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>Low Stock:</b> ${lowStock}
    `;
}

function showProductModal() {
    document.getElementById("productModal").style.display = "block";
}

function closeModal() {
    document.getElementById("productModal").style.display = "none";
}

async function saveProduct() {

    const payload = {
        name: name.value,
        sku: sku.value,
        category: category.value,
        quantity: quantity.value,
        buying_price: buying_price.value,
        selling_price: selling_price.value,
        supplier: supplier.value,
        company_id: 1
    };

    const res = await fetch("/api/inventory", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(payload)
    });

    const out = await res.json();

    if (out.status === "success") {
        closeModal();
        loadInventory();
    } else {
        alert(out.message || "Error");
    }
}

loadInventory();
