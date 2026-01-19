document.addEventListener("DOMContentLoaded", () => {
  showPage("dashboard");
});

document.addEventListener("DOMContentLoaded", fetchDashboardData);

function showPage(page) {
  // Hide all pages
  document.querySelectorAll(".page").forEach((p) => {
    p.style.display = "none";
  });

  // Show selected page
  const selectedPage = document.getElementById(page);
  if (selectedPage) {
    selectedPage.style.display = "block";
  }

  // Remove active class from menu
  document.querySelectorAll(".menu li").forEach((li) => {
    li.classList.remove("active");
  });

  // Add active class to current menu
  document
    .querySelector(`.menu li[data-page="${page}"]`)
    ?.classList.add("active");
}

const modal = document.getElementById("assetModal");
const openBtn = document.getElementById("openModal");
const closeBtn = document.querySelector(".close");
const cancelBtn = document.querySelector(".cancel");

openBtn.onclick = () => (modal.style.display = "block");
closeBtn.onclick = cancelBtn.onclick = () => (modal.style.display = "none");

window.onclick = (e) => {
  if (e.target === modal) modal.style.display = "none";
};

// Submit (later connect to FastAPI)
document
  .getElementById("assetForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault(); // prevent page reload

    const assetData = {
      name: document.getElementById("assetName").value,
      category: document.getElementById("category").value,
      brand: document.getElementById("brand").value || null,
      serialno: document.getElementById("serialNumber").value,
      status: document.getElementById("status").value, // "Active" or "Expired"
      purchasedate: document.getElementById("purchaseDate").value, // YYYY-MM-DD
      expirydate: document.getElementById("expiryDate").value || null,
      warrentyexpiry: document.getElementById("warrantyExpiry").value || null,
      notes: document.getElementById("notes").value || null,
      compliance_status:
        document.getElementById("complianceStatus").value || null,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/assets/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(assetData),
      });

      const result = await response.json();
      console.log(result);
      alert(result.assetid); // or display it somewhere in the page

      // Optionally reset the form
      document.getElementById("assetForm").reset();

      fetchDashboardData();
      loadAssets();
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to add asset.");
    }
  });

async function fetchDashboardData() {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/dashboard");
    const data = await response.json();

    console.log(data);

    document.getElementById("total_assets").innerText = data.total_assets;
    document.getElementById("active_assets").innerText = data.active_assets;
    document.getElementById("near_expiry").innerText = data.active_assets;
    document.getElementById("expired").innerText = data.expired_assets;
    document.getElementById("compliant").innerText = data.Compliant;
    document.getElementById("non_compliant").innerText = data.Non_Compliant;
    document.getElementById("pending_review").innerText = data.Pending_Review;

    if (data != null) {
      document.getElementById("emptyAssets").style.display = "none";
      updateAssetTableData(data.tenassets);
    }
  } catch (error) {
    console.error("Failed to load dashboard data", error);
  }
}

function updateAssetTableData(dataForTable) {
  const tableBody = document.getElementById("recentAssets");

  for (let asset of dataForTable.slice().reverse()) {
    const assetId = asset.assetid;
    const name = asset.name;
    const category = asset.category;
    const status = asset.status;

    const row = `
    <tr>
      <td>${assetId}</td>
      <td class="bold">${name.toUpperCase()}</td>
      <td>${category}</td>
      <td><span class="badge active">${status}</span></td>
    </tr>
  `;

    tableBody.insertAdjacentHTML("afterbegin", row);
  }
}

// For Assets

function renderAssets(assets) {
  const container = document.getElementById("assetsRows");
  container.innerHTML = ""; // clear old rows

  assets.forEach((asset) => {
    console.log(asset);
    const row = document.createElement("div");
    row.className = "asset-row";

    row.innerHTML = `
      <div class="mono">${asset.assetid}</div>
      <div class="bold">${asset.name.toUpperCase()}</div>
      <div>${asset.category}</div>
      <div>${asset.brand || "-"}</div>

      <div>
        <span class="pill ${asset.status === "Active" ? "success" : "danger"}">
          ${asset.status}
        </span>
      </div>

      <div>
        <span class="pill ${getComplianceClass(asset.compliance_status)}">
          ${asset.compliance_status}
        </span>
      </div>

      <div>${asset.expirydate || "-"}</div>
      <div class="dots">⋯</div>
    `;

    container.appendChild(row);
  });
}

function getComplianceClass(status) {
  if (status === "Compliant") return "success";
  if (status === "Pending Review") return "warning";
  if (status === "Non-Compliant") return "danger";
  return "";
}

async function loadAssets() {
  try {
    const res = await fetch("http://127.0.0.1:8000/api/v1/assets/");
    const data = await res.json();

    renderAssets(data); // 🔥 dynamic injection
  } catch (err) {
    console.error("Failed to load assets", err);
  }
}

loadAssets();

const openBtnInAssset = document.getElementById("openModalInAssets");
openBtnInAssset.onclick = () => (modal.style.display = "block");

const categ = document.getElementById("categ");
const stat = document.getElementById("stat");

/* 🔹 Category change */
categ.addEventListener("change", () => {
  const selectedValueCateg = categ.value;
  const selectedValueStat = stat.value;

  if (selectedValueCateg === "all" && selectedValueStat === "all") {
    loadAssets();
  } else if (selectedValueCateg === "all") {
    searchAndUpdatebyStat(selectedValueStat);
  } else if (selectedValueStat === "all") {
    searchAndUpdatebyCat(selectedValueCateg);
  } else {
    searchAssets(selectedValueCateg, selectedValueStat);
  }
});

/* 🔹 Status change */
stat.addEventListener("change", () => {
  const selectedValueStat = stat.value;
  const selectedValueCateg = categ.value;

  if (selectedValueCateg === "all" && selectedValueStat === "all") {
    loadAssets();
  } else if (selectedValueCateg === "all") {
    searchAndUpdatebyStat(selectedValueStat);
  } else if (selectedValueStat === "all") {
    searchAndUpdatebyCat(selectedValueCateg);
  } else {
    searchAssets(selectedValueCateg, selectedValueStat);
  }
});

/* 🔹 Category + Status */
async function searchAssets(selectedValueCateg, selectedValueStat) {
  try {
    const res = await fetch(
      `http://127.0.0.1:8000/api/v1/assets/assetbycatANDstat/${selectedValueCateg}/${selectedValueStat}`
    );
    const data = await res.json();
    renderAssets(data);
  } catch (err) {
    console.error("Failed to load assets", err);
  }
}

/* 🔹 Category only */
async function searchAndUpdatebyCat(selectedValueCateg) {
  try {
    const res = await fetch(
      `http://127.0.0.1:8000/api/v1/assets/assetbycat/${encodeURIComponent(
        selectedValueCateg
      )}`
    );
    const data = await res.json();
    renderAssets(data);
  } catch (err) {
    console.error("Failed to load assets", err);
  }
}

/* 🔹 Status only */
async function searchAndUpdatebyStat(selectedValueStat) {
  try {
    const res = await fetch(
      `http://127.0.0.1:8000/api/v1/assets/assetbystat/${encodeURIComponent(
        selectedValueStat
      )}`
    );
    const data = await res.json();
    renderAssets(data);
  } catch (err) {
    console.error("Failed to load assets", err);
  }
}

document
  .getElementById("asset-search")
  .addEventListener("input", debounce(handleAssetSearch, 300));

async function handleAssetSearch(e) {
  const query = e.target.value.trim();

  // If search is empty → load all assets
  if (query.length === 0) {
    loadAssets();
    return;
  }

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/v1/assets/searchbyInputs?q=${encodeURIComponent(query)}`
    );

    if (!response.ok) {
      throw new Error("Asset search failed");
    }

    const data = await response.json();
    console.log(data)
    renderAssets(data);

  } catch (err) {
    console.error(err);
  }
}



//   Employee



document.getElementById("employeesClick").addEventListener("click", () => {
  loadEmployees();
});


// EMPLOYEE MODAL
const empModal = document.getElementById("employeeModal");
const empOpenBtn = document.getElementById("openEmployeeModal");
const empCloseBtn = empModal.querySelector(".close");
const empCancelBtn = empModal.querySelector(".emp-btn-cancel");

empOpenBtn.onclick = () => (empModal.style.display = "block");

empCloseBtn.onclick = empCancelBtn.onclick = () =>
  (empModal.style.display = "none");

window.addEventListener("click", (e) => {
  if (e.target === empModal) {
    empModal.style.display = "none";
  }
});


// EMPLOYEE FORM SUBMIT
document
  .getElementById("employeeForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault(); // prevent reload

    const employeeData = {
      fullname: document.getElementById("fullName").value,
      email: document.getElementById("email").value || null,
      department: document.getElementById("department").value || null,
      role: document.getElementById("position").value || null,
    };

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/employees/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(employeeData),
        }
      );

      const result = await response.json();

      alert("Employee created successfully");

      // Reset & close
      document.getElementById("employeeForm").reset();
      empModal.style.display = "none";

      // Reload employee list
      loadEmployees();

    } catch (error) {
      console.error("Error:", error);
      alert("Failed to add employee");
    }
  })

async function loadEmployees() {
  try {
    const res = await fetch("http://127.0.0.1:8000/api/employees/");
    const data = await res.json();

    renderemployees(data); // 🔥 dynamic injection
  } catch (err) {
    console.error("Failed to load employees", err);
  }
}

  const employeeRows = document.getElementById("employeeRows");
  
  function renderemployees(data) {
    employeeRows.innerHTML=""
    if (data){
      document.getElementById("em-empty").style.display="none"
    }else{
      document.getElementById("emp-list").style.display="none"

    }


   data.forEach((emp) => {
    const row = document.createElement("div");
  row.className = "employee-row data";

  row.innerHTML = `
    <div class="employee-id">${emp.employeeid}</div>
    <div class="employee-name">${emp.fullname}</div>
    <div>${emp.email || "-"}</div>
    <div>${emp.department || "-"}</div>
    <div>${emp.role || "-"}</div>
  `;

  employeeRows.appendChild(row);})
}

document
  .getElementById("emp-search")
  .addEventListener("input", debounce(handleEmployeeSearch, 300));

async function handleEmployeeSearch(e) {
  const query = e.target.value.trim();

  // If search is empty → load all employees
  if (query.length === 0) {
    loadEmployees();
    return;
  }

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/employees/search?q=${encodeURIComponent(query)}`
    );

    if (!response.ok) {
      throw new Error("Search failed");
    }

    const data = await response.json();
    renderemployees(data);

  } catch (err) {
    console.error(err);
  }
}



function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}


//  Expiry Tracking


document.getElementById("ExpiryTrackingClick").addEventListener("click", () => {
loadExpiryTracking();
loadExpirySoonTracking();
});

async function loadExpiryTracking() {
  try {
    const res = await fetch(
      "http://127.0.0.1:8000/expirytracking/expirydetails"
    );
    const assets = await res.json();
    console.log(assets)
    // Render BOTH tables
    renderExpiryTable(assets, "expiredList", "expired");

  } catch (err) {
    console.error("Failed to load expiry tracking", err);
  }
}

async function loadExpirySoonTracking() {
  try {
    const res = await fetch(
      "http://127.0.0.1:8000/expirytracking/expirysoon"
    );
    const assets = await res.json();

    // Render BOTH tables
    renderExpiryTable(assets, "expiringList", "expiring");

  } catch (err) {
    console.error("Failed to load expiry tracking", err);
  }
}


function renderExpiryTable(assets, containerId, mode) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";

  let count = 0;

  assets.forEach(asset => {
  console.log(asset)
    const row = `
      <div class="expiry-row">
        <div class="name"> ${asset.assetname.toUpperCase()}</div>
        <div class="date">${asset.expireddate}</div>
        <div class="status">
          <span class="badge ${mode}"}">
            ${mode}
          </span>
        </div>
      </div>
    `;

    container.insertAdjacentHTML("beforeend", row);
    count++;
  });

  // Empty state
  if (count === 0) {
    container.innerHTML = `
      <p class="empty">
        ${mode === "expired"
          ? "No expired assets"
          : "No assets expiring soon"}
      </p>`;
  }

  // Update count heading
  document.getElementById(
    mode === "expired" ? "expiredCount" : "expiringCount"
  ).innerText =
    mode === "expired"
      ? `Expired Assets (${count})`
      : `Expiring Soon - 30 Days (${count})`;
}


//  Assignment

const assignModal = document.getElementById("assignAssetModal");

document
  .getElementById("openAssignModal")
  .addEventListener("click", () => {
    assignModal.classList.add("active");
  });

document
  .getElementById("closeAssignModal")
  .addEventListener("click", closeAssignModal);

document
  .getElementById("cancelAssign")
  .addEventListener("click", closeAssignModal);

function closeAssignModal() {
  assignModal.classList.remove("active");
}




 // Load assignments when page is opened
document.getElementById("assignmentClick").addEventListener("click", () => {
  loadAssignments();
});

async function loadAssignments() {
  try {
    const res = await fetch("http://127.0.0.1:8000/api/v1/assignment/");
    const data = await res.json();
    console.log(data)
    renderAssignments(data);
  } catch (err) {
    console.error("Failed to load assignments", err);
  }
}


function renderAssignments(assignments) {
  const container = document.getElementById("assignmentTableBody");
  container.innerHTML = "";

  if (!assignments.length) {
    container.innerHTML = `
      <tr>
        <td colspan="6" style="text-align:center; padding:20px;">
          No assignments found
        </td>
      </tr>
    `;
    return;
  }

  assignments.forEach(assign => {
    container.innerHTML += `
      <tr>
        <td class="mono">${assign.assetid}</td>
        <td class="assignment-asset-name">${assign.assetname}</td>
        <td>${assign.employeename}</td>
        <td>${formatDate(assign.assigneddate)}</td>
        <td>${assign.actualreturndate ? formatDate(assign.actualreturndate) : "-"}</td>
        <td>
          <span class="assignment-status ${assign.assignmentstatus.toLowerCase()}">
            ${assign.assignmentstatus}
          </span>
        </td>
      </tr>
    `;
  });
}



function getAssignStatusClass(status) {
    switch (status) {
        case "Assigned":
            return "status-assigned";
        case "Returned":
            return "status-returned";
        case "Lost":
            return "status-lost";
        case "Damaged":
            return "status-damaged";
        default:
            return "";
    }
}


  


function formatDate(dateString) {
    if (!dateString) return "-";
    const date = new Date(dateString);
    return date.toLocaleDateString("en-IN");
}


async function loadAssetOptions() {
  try {
    const res = await fetch("http://127.0.0.1:8000/api/v1/assets");
    const data = await res.json();

    const select = document.getElementById("assetSelect");
    select.innerHTML = `<option value="">Select Asset</option>`;

    data.forEach(asset => {
      const option = document.createElement("option");
      option.value = asset.assetid;
      option.textContent = `${asset.name}(${asset.assetid})`;
      select.appendChild(option);
    });
  } catch (err) {
    console.error("Failed to load assets", err);
  }
}

document.addEventListener("DOMContentLoaded", loadAssetOptions);


async function loadEmployeeOptions() {
  try {
    const res = await fetch("http://127.0.0.1:8000/api/employees");
    const employees = await res.json();

    const select = document.getElementById("employeeSelect");
    select.innerHTML = `<option value="">Select Employee</option>`;

    employees.forEach(emp => {
      const option = document.createElement("option");
      option.value = emp.employeeid;   // adjust if your key differs
      option.textContent = `${emp.fullname}(${emp.employeeid})`;
      select.appendChild(option);
    });
  } catch (err) {
    console.error("Failed to load employees", err);
  }
}

document.addEventListener("DOMContentLoaded", loadEmployeeOptions);


//  Reports

function exportAuditReport() {
  window.location.href = "http://127.0.0.1:8000/reports/assets/export";
}

function exportOwnershipReport() {
  window.location.href = "http://127.0.0.1:8000/reports/ownership/export";
}

function exportExpiryReport() {
  window.location.href = "http://127.0.0.1:8000/reports/expiry-compliance/export";
}
