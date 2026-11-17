async function request(path, options = {}) {
    const response = await fetch(path, {
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        },
        ...options
    });


    if (response.status === 204) {
        return null;
    }


    const data = await response.json();


    if (!response.ok) {
        console.error("API request failed:", {
            path,
            status: response.status,
            response: data
        });


        let message = "The request failed.";


        if (typeof data.detail === "string") {
            message = data.detail;
        } else if (Array.isArray(data.detail)) {
            message = data.detail
                .map((item) => {
                    const location = item.loc.join(" -> ");

                    return `${location}: ${item.msg}`;
                })
                .join("; ");
        }

        throw new Error(message);
    }

    return data;
}




export function searchTransactions(
    source,
    searchTerm = "",
    limit = 500
) {
    const parameters = new URLSearchParams();


    if (searchTerm.trim()) {
        parameters.set(
            "q",
            searchTerm.trim()
        );
    }


    parameters.set(
        "limit",
        String(limit)
    );


    return request(
        `/api/search/${source}?${parameters.toString()}`
    );
}




export function updateTransaction(
    transactionId,
    updates
) {
    return request(
        `/api/transactions/${transactionId}`,
        {
            method: "PATCH",
            body: JSON.stringify(updates)
        }
    );
}
