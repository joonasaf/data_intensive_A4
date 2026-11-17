import {
  useEffect,
  useState
} from "react";


import {
  searchTransactions,
  updateTransaction
} from "./api";



const DATA_SOURCES = {
  all: {
    title: "All Data",
    description:
    "Unique records from PostgreSQL and MongoDB."
  },

  sql: {
    title: "PostgreSQL",
    description:
    "Records stored in the SQL database."
  },

  nosql: {
    title: "MongoDB",
    description:
    "Documents stored in the NoSQL database."
  }
};




const TABLE_COLUMNS = [
  {
    key: "transaction_id",
    label: "Transaction ID"
  },
  {
    key: "customer_name",
    label: "Customer"
  },
  {
    key: "order_date",
    label: "Order Date"
  },
  {
    key: "product_name",
    label: "Product"
  },
  {
    key: "quantity",
    label: "Quantity"
  },
  {
    key: "sales_amount",
    label: "Sales Amount"
  },
  {
    key: "order_status",
    label: "Status"
  },
  {
    key: "storage_type",
    label: "Storage"
  },
  {
    key: "version",
    label: "Version"
  },
  {
    key: "source",
    label: "Source"
  }
];




const EDIT_FIELDS = [
  {
    key: "order_id",
    label: "Order ID",
    type: "text"
  },
  {
    key: "customer_id",
    label: "Customer ID",
    type: "text"
  },
  {
    key: "customer_name",
    label: "Customer Name",
    type: "text"
  },
  {
    key: "customer_age",
    label: "Customer Age",
    type: "number"
  },
  {
    key: "customer_gender",
    label: "Customer Gender",
    type: "text"
  },
  {
    key: "customer_segment",
    label: "Customer Segment",
    type: "text"
  },
  {
    key: "order_date",
    label: "Order Date",
    type: "date"
  },
  {
    key: "order_time",
    label: "Order Time",
    type: "time"
  },
  {
    key: "sales_channel",
    label: "Sales Channel",
    type: "text"
  },
  {
    key: "store_id",
    label: "Store ID",
    type: "text"
  },
  {
    key: "store_name",
    label: "Store Name",
    type: "text"
  },
  {
    key: "country",
    label: "Country",
    type: "text"
  },
  {
    key: "region",
    label: "Region",
    type: "text"
  },
  {
    key: "city",
    label: "City",
    type: "text"
  },
  {
    key: "product_id",
    label: "Product ID",
    type: "text"
  },
  {
    key: "product_name",
    label: "Product Name",
    type: "text"
  },
  {
    key: "product_category",
    label: "Product Category",
    type: "text"
  },
  {
    key: "product_subcategory",
    label: "Product Subcategory",
    type: "text"
  },
  {
    key: "quantity",
    label: "Quantity",
    type: "number"
  },
  {
    key: "unit_price",
    label: "Unit Price",
    type: "number",
    step: "0.01"
  },
  {
    key: "discount_percentage",
    label: "Discount Percentage",
    type: "number",
    step: "0.01"
  },
  {
    key: "sales_amount",
    label: "Sales Amount",
    type: "number",
    step: "0.01"
  },
  {
    key: "cost_amount",
    label: "Cost Amount",
    type: "number",
    step: "0.01"
  },
  {
    key: "profit",
    label: "Profit",
    type: "number",
    step: "0.01"
  },
  {
    key: "payment_method",
    label: "Payment Method",
    type: "text"
  },
  {
    key: "order_status",
    label: "Order Status",
    type: "text"
  },
  {
    key: "shipping_method",
    label: "Shipping Method",
    type: "text"
  },
  {
    key: "delivery_days",
    label: "Delivery Days",
    type: "number"
  },
  {
    key: "return_flag",
    label: "Return Flag",
    type: "text"
  },
  {
    key: "return_reason",
    label: "Return Reason",
    type: "text",
    optional: true
  },
  {
    key: "sales_representative",
    label: "Sales Representative",
    type: "text"
  },
  {
    key: "promotion_code",
    label: "Promotion Code",
    type: "text",
    optional: true
  },
  {
    key: "customer_rating",
    label: "Customer Rating",
    type: "number",
    step: "0.1"
  },
  {
    key: "inventory_level",
    label: "Inventory Level",
    type: "number"
  },
  {
    key: "order_year",
    label: "Order Year",
    type: "number"
  }
];




const INTEGER_FIELDS = new Set([
  "customer_age",
  "quantity",
  "delivery_days",
  "inventory_level",
  "order_year"
]);




const FLOAT_FIELDS = new Set([
  "unit_price",
  "discount_percentage",
  "sales_amount",
  "cost_amount",
  "profit",
  "customer_rating"
]);




function normalizeFieldValue(
  fieldName,
  value
) {
  if (INTEGER_FIELDS.has(fieldName)) {
    return Number.parseInt(
      value,
      10
    );
  }


  if (FLOAT_FIELDS.has(fieldName)) {
    return Number.parseFloat(value);
  }


  if (
    fieldName === "return_reason"
    || fieldName === "promotion_code"
  ) {
    return value.trim() === ""
      ? null
      : value;
  }


  return value;
}




function formatTableValue(
  record,
  columnKey
) {
  const value = record[columnKey];


  if (
    columnKey === "sales_amount"
    && value !== undefined
    && value !== null
  ) {
    return Number(value).toFixed(2);
  }


  if (
    value === null
    || value === undefined
    || value === ""
  ) {
    return "—";
  }


  return value;
}




function App() {
  const [
    selectedSource,
    setSelectedSource
  ] = useState("all");


  const [
    records,
    setRecords
  ] = useState([]);


  const [
    searchInput,
    setSearchInput
  ] = useState("");


  const [
    activeSearchTerm,
    setActiveSearchTerm
  ] = useState("");


  const [
    loading,
    setLoading
  ] = useState(false);


  const [
    error,
    setError
  ] = useState("");


  const [
    successMessage,
    setSuccessMessage
  ] = useState("");


  const [
    editingId,
    setEditingId
  ] = useState(null);


  const [
    formData,
    setFormData
  ] = useState({});


  const [
    originalData,
    setOriginalData
  ] = useState({});




  const sourceConfiguration =
    DATA_SOURCES[selectedSource];




  useEffect(() => {
    resetForm();
    loadRecords();
  }, [
    selectedSource,
    activeSearchTerm
  ]);




  async function loadRecords() {
    setLoading(true);
    setError("");


    try {
      const data = await searchTransactions(
        selectedSource,
        activeSearchTerm,
        500
      );

      setRecords(data);

    } catch (requestError) {
      setError(requestError.message);

    } finally {
      setLoading(false);
    }
  }


  function handleSearchSubmit(event) {
    event.preventDefault();


    setSuccessMessage("");
    setActiveSearchTerm(
      searchInput.trim()
    );
  }


  function clearSearch() {
    setSearchInput("");
    setActiveSearchTerm("");
  }


  function handleInputChange(event) {
    const {
      name,
      value
    } = event.target;

    setFormData(
      (currentData) => ({
        ...currentData,
        [name]: value
      })
    );
  }


  function startEditing(record) {
    const editableData = {};

    EDIT_FIELDS.forEach((field) => {
      const value = record[field.key];

      editableData[field.key] =
        value ?? "";
    });

    setEditingId(
      record.transaction_id
    );

    setFormData(editableData);
    setOriginalData(editableData);

    setError("");
    setSuccessMessage("");

    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  }


  function resetForm() {
    setEditingId(null);
    setFormData({});
    setOriginalData({});
  }


  function buildPatchPayload() {
    const updates = {};


    EDIT_FIELDS.forEach((field) => {
      const fieldName = field.key;


      const currentValue =
        formData[fieldName] ?? "";


      const originalValue =
        originalData[fieldName] ?? "";


      if (
        String(currentValue)
        !== String(originalValue)
      ) {
        updates[fieldName] =
          normalizeFieldValue(
            fieldName,
            currentValue
          );
      }
    });


    return updates;
  }


  async function handleUpdateSubmit(event) {
    event.preventDefault();

    setError("");
    setSuccessMessage("");

    const updates = buildPatchPayload();

    if (
      Object.keys(updates).length === 0
    ) {
      setError("No changes were made.");

      return;
    }

    try {
      const updatedRecord =
        await updateTransaction(
          editingId,
          updates
        );

      setSuccessMessage(
        `Transaction ${editingId} was updated. `
        + `Version is now ${updatedRecord.version}.`
      );

      resetForm();

      await loadRecords();

    } catch (requestError) {
      setError(requestError.message);
    }
  }


  return (
    <main className="app">


      <header className="page-header">
        <h1>
          SQL and NoSQL Sales Data System
        </h1>

        <p className="subtitle">
          Search and modify data stored in
          PostgreSQL and MongoDB.
        </p>
      </header>


      <nav className="database-tabs">
        <button
          type="button"
          className={
            selectedSource === "all"
              ? "database-tab active"
              : "database-tab"
          }
          onClick={() =>
            setSelectedSource("all")
          }
        >
          All Data
        </button>


        <button
          type="button"
          className={
            selectedSource === "sql"
              ? "database-tab active"
              : "database-tab"
          }
          onClick={() =>
            setSelectedSource("sql")
          }
        >
          PostgreSQL
        </button>


        <button
          type="button"
          className={
            selectedSource === "nosql"
            ? "database-tab active"
            : "database-tab"
          }
          onClick={() =>
            setSelectedSource("nosql")
          }
        >
          MongoDB
        </button>
      </nav>




      <form
        className="search-form"
        onSubmit={handleSearchSubmit}
      >
        <input
          type="search"
          value={searchInput}
          onChange={(event) =>
            setSearchInput(
              event.target.value
            )
          }
          placeholder={
            "Search transactions, customers, "
            + "products, cities or values..."
          }
        />


        <button
          className="primary-button"
          type="submit"
        >
          Search
        </button>


        <button
          className="secondary-button"
          type="button"
          onClick={clearSearch}
        >
          Clear
        </button>
      </form>


      {error && (
        <div className="error-message">
          {error}
        </div>
      )}


      {successMessage && (
        <div className="success-message">
          {successMessage}
        </div>
      )}


      <div className="content-grid">

        <section className="card records-card">

          <div className="section-header">
            <div>
              <p className="subtitle">
                Selected source
              </p>

              <h2>
              {sourceConfiguration.title}
              </h2>

              <p className="source-description">
                {
                  sourceConfiguration
                    .description
                }
              </p>
            </div>

            <button
              type="button"
              className="secondary-button"
              onClick={loadRecords}
            >
              Refresh
            </button>
          </div>


          <p className="result-count">
            {records.length} records displayed
          </p>




          {loading ? (
          <p className="status-message">
            Loading records...
          </p>

          ) : records.length === 0 ? (
            <p className="status-message">
              No matching records found.
            </p>


          ) : (
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    {TABLE_COLUMNS.map(
                      (column) => (
                        <th key={column.key}>
                          {column.label}
                        </th>
                      )
                    )}

                    <th>Actions</th>
                  </tr>
                </thead>

                <tbody>
                  {records.map((record) => (
                    <tr
                      key={
                        record.transaction_id
                      }
                    >
                      {TABLE_COLUMNS.map(
                        (column) => (
                          <td key={column.key}>
                            {formatTableValue(
                              record,
                              column.key
                            )}
                          </td>
                        )
                      )}

                      <td className="actions">
                        <button
                          type="button"
                          className="edit-button"
                          onClick={() =>
                            startEditing(record)
                          }
                        >
                          Edit
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>


        <section className="card form-card">

          {editingId === null ? (
            <>
              <p className="subtitle">
                Modification
              </p>

              <h2>
              Select a Record
              </h2>

              <p className="status-message">
                Select Edit next to a transaction
                to modify its data.
              </p>
            </>

          ) : (
            <>
              <p className="subtitle">
                Editing transaction
              </p>

              <h2>
                {editingId}
              </h2>

              <form
                className="record-form"
                onSubmit={handleUpdateSubmit}
              >
                {EDIT_FIELDS.map((field) => (
                  <label
                    className="form-field"
                    key={field.key}
                    htmlFor={field.key}
                  >
                    {field.label}

                    <input
                      id={field.key}
                      type={field.type}
                      name={field.key}
                      step={field.step}
                      required={!field.optional}
                      value={
                        formData[field.key]
                        ?? ""
                      }
                      onChange={
                        handleInputChange
                      }
                    />
                  </label>
                ))}


                <div className="form-actions">
                  <button
                    className="primary-button"
                    type="submit"
                  >
                    Save Changes
                  </button>


                  <button
                    className="secondary-button"
                    type="button"
                    onClick={resetForm}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </>
          )}
        </section>

      </div>

    </main>
  );
}


export default App;
