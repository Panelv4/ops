const searchBox = document.querySelector(".search-box");

if (searchBox) {

    let resultBox = document.createElement("div");
    resultBox.id = "searchResults";
    resultBox.className = "search-results";

    searchBox.parentNode.appendChild(resultBox);

    searchBox.addEventListener("keyup", async function () {

        const q = this.value.trim();

        if (q.length < 2) {
            resultBox.innerHTML = "";
            return;
        }

        try {

            const data = await API.get("/api/search?q=" + encodeURIComponent(q));

            let html = "";

            data.forEach(item => {
                html += `
                    <div class="search-item">
                        <b>${item.module}</b><br>
                        ${item.name}
                    </div>
                `;
            });

            resultBox.innerHTML = html;

        } catch (e) {
            resultBox.innerHTML = "";
        }

    });

}
