document.addEventListener("DOMContentLoaded", function () {

    const currentPath = window.location.pathname;

    // Only handle recommendation forms
    if (
        currentPath !== "/home" &&
        currentPath !== "/party" &&
        currentPath !== "/jewelry"
    ) {
        return;
    }

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener("submit", async function (event) {

            event.preventDefault();

            const budget = document.getElementById("budget").value;
            const preferences = document.getElementById("preferences").value;
            const resultBox = document.getElementById("recommendation-result");

            let apiUrl = "";
            let category = "";

            if (currentPath === "/home") {
                apiUrl = "/generate-home";
                category = "Home Decor";
            } else if (currentPath === "/party") {
                apiUrl = "/generate-party";
                category = "Party Planning";
            } else if (currentPath === "/jewelry") {
                apiUrl = "/generate-jewelry";
                category = "Jewelry";
            }

            if (!apiUrl) {
                return;
            }

            resultBox.innerHTML =
                "<p>🤖 Generating recommendations...</p>";

            try {

                const response = await fetch(apiUrl, {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        category: category,
                        budget: Number(budget),
                        preferences: preferences
                    })
                });

                const contentType = response.headers.get("content-type") || "";
                let data;

                if (contentType.includes("application/json")) {
                    data = await response.json();
                } else {
                    const text = await response.text();
                    throw new Error(
                        text || `Request failed with status ${response.status}`
                    );
                }

                if (!response.ok) {
                    throw new Error(
                        data.detail || `Request failed with status ${response.status}`
                    );
                }

                resultBox.innerHTML = `
                    <div class="recommendation-box">

                        <h2>✨ AI Recommendations</h2>

                        <p>
                            <strong>Category:</strong>
                            ${data.category}
                        </p>

                        <p>
                            <strong>Budget:</strong>
                            ₹${data.budget}
                        </p>

                        <div class="recommendation-text">
                            ${data.recommendations.replace(/\n/g, "<br>")}
                        </div>

                    </div>
                `;

            } catch (error) {

                resultBox.innerHTML = `
                    <div class="recommendation-box">

                        <h2>❌ Error</h2>

                        <p>${error.message}</p>

                    </div>
                `;

            }

        });

    });

});