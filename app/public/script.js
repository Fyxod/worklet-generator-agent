const fileInput = document.getElementById("file-input");
const fileList = document.getElementById("file-list");
const form = document.getElementById("worklet-form");
const loading = document.getElementById("loading");
const progressContainer = document.getElementById("progress-container");
const progressBar = document.getElementById("progress-bar");
const progressMessage = document.getElementById("progress-message");
const downloadList = document.getElementById("download-list");
const genWorkButton = document.getElementById("gen-work");
const clearButton = document.getElementById("clear-but");
let sid = "";
const socket = io("/", {
  transports: ["websocket"],
});

socket.on("connect", () => {
  console.log("Connected to server");
  sid = socket.id;
});
socket.on("disconnect", () => {
  console.log("Disconnected from server");
});
socket.on("heartbeat", (data) => {
  console.log("Heartbeat:", data.status);
});

let selectedFiles = [];
let totalWorklets = 5;
let generatedCount = 0;
let errorOccurred = false;
let receivedFiles = [];

socket.on("total_worklets", (data) => {
  console.log("Total worklets:", data.total_worklets);
  totalWorklets = data.total_worklets;
});

fileInput.addEventListener("change", (e) => {
  selectedFiles = Array.from(e.target.files);
  renderFileList();
});

function renderFileList() {
  fileList.innerHTML = "";
  selectedFiles.forEach((item, index) => {
    const wrapper = document.createElement("div");
    const fileLabel = document.createElement("div");
    fileLabel.className = "file-name";
    let sizeInKB = item.size / 1024;
    let sizeText;

    if (sizeInKB < 1024) {
      sizeText = sizeInKB.toFixed(1) + " KB";
    } else {
      let sizeInMB = sizeInKB / 1024;
      sizeText = sizeInMB.toFixed(1) + " MB";
    }

    fileLabel.textContent = item.name + " (" + sizeText + ")";

    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.textContent = "✖";
    removeButton.onclick = () => {
      selectedFiles.splice(index, 1);
      renderFileList();
    };

    wrapper.appendChild(fileLabel);
    wrapper.appendChild(removeButton);
    fileList.appendChild(wrapper);
  });
}

function removeFile(index) {
  selectedFiles.splice(index, 1);
  renderFileList();
}

function addLinkField() {
  const div = document.createElement("div");
  div.innerHTML = `
      <input type="url" name="links[]" placeholder="Enter link">
      <button type="button" class="remove-link-btn" onclick="removeLinkField(this)">✖</button>
    `;
  document.getElementById("link-fields").appendChild(div);
}

function removeLinkField(button) {
  button.parentElement.remove();
}

function clearAll() {
  window.location.reload(); // Reload the page to clear everything
  generatedCount = 0;
  errorOccurred = true;

  fileInput.value = "";
  selectedFiles = [];

  renderFileList();

  const modelSelect = document.getElementById("model-select");
  fileList.innerHTML = "";
  loading.style.display = "none";
  progressContainer.style.display = "none";
  progressBar.style.width = "0%";
  progressMessage.style.display = "none";
  progressMessage.textContent = "Sending...";
  downloadList.innerHTML = "";
  fileInput.value = "";

  const linkFields = document.getElementById("link-fields");
  linkFields.innerHTML = `
      <div>
        <input type="url" name="links[]" placeholder="Enter link">
        <button type="button" class="remove-link-btn" onclick="removeLinkField(this)">✖</button>
      </div>
    `;

  downloadList.innerHTML = "";
}

socket.on("pdf_generated", (data) => {
  if (errorOccurred) return;
  console.log("PDF generated:", data);
  generatedCount++;
  updateLoadingText();

  if (data.file_name) {
    const a = document.createElement("a");
    a.href = `/download/${encodeURIComponent(data.file_name)}`;
    a.download = data.file_name;
    a.style.animation = "fadeIn 0.6s ease forwards";
    a.style.display = "flex";
    a.style.alignItems = "center";
    a.style.gap = "8px";

    const icon = document.createElement("img");
    icon.src = "/static/icon.png";
    icon.alt = "File Icon";
    icon.style.width = "20px";
    icon.style.height = "20px";

    const fileName = document.createElement("span");
    fileName.textContent = data.file_name;

    a.appendChild(icon);
    a.appendChild(fileName);

    downloadList.appendChild(a);
  }

  const percent = (generatedCount / totalWorklets) * 100;
  progressBar.style.width = `${percent}%`;
});

socket.on("progress", (data) => {
  if (errorOccurred) return;
  console.log("Progress:", data);
  if (progressMessage.style.display !== "none") {
    progressMessage.style.animation = "none";
    void progressMessage.offsetWidth;
    progressMessage.style.animation = "fadeIn 0.6s ease forwards";
    progressMessage.textContent = data.message || "Processing...";
  }
});
socket.on("fileReceived", (data) => {
  if (errorOccurred) return;
  console.log("File received:", data);
  receivedFiles.push(data.file_name);
});

socket.on("error", (data) => {
  console.error("Error event received:", data);
  errorOccurred = true;

  loading.style.display = "none";
  progressContainer.style.display = "none";

  progressMessage.style.display = "block";
  progressMessage.style.animation = "none";
  void progressMessage.offsetWidth;
  progressMessage.style.animation = "fadeIn 0.6s ease forwards";
  progressMessage.textContent = data.message || "An unknown error occurred.";
});

function updateLoadingText() {
  loading.textContent = `🔄 Generating Worklets... (${generatedCount}/${totalWorklets} done)`;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  progressBar.style.width = "0%";
  loading.style.display = "none";
  loading.textContent = "";
  errorOccurred = false; // reset before sending
  generatedCount = 0; // reset count before sending
  receivedFiles = []; // reset received files

  const linkInputs = document.querySelectorAll('input[name="links[]"]');
  let links = [];
  linkInputs.forEach((input) => {
    if (input.value.trim()) links.push(input.value.trim());
  });

  const customPrompt = document.getElementById("custom-prompt")?.value || "";
  if (selectedFiles.length === 0 && links.length === 0 && !customPrompt) {
    alert(
      "Please upload at least one file or enter at least one link or a custom prompt."
    );
    return;
  }

  const formData = new FormData();
  selectedFiles.forEach((file) => {
    if (file.size > 100 * 1024 * 1024) {
      alert(`File ${file.name} exceeds 100MB limit.`);
      return;
    }
    formData.append("files", file);
  });

  const model = document.getElementById("model-select").value;

  formData.append("links", JSON.stringify(links));
  formData.append("sid", socket.id);

  loading.style.display = "block";
  progressContainer.style.display = "block";
  progressMessage.style.display = "block";
  progressMessage.textContent = "Sending...";
  downloadList.innerHTML = "";

  try {
    formData.append("custom_prompt", customPrompt);

    genWorkButton.classList.add("hidden");
    clearButton.classList.add("hidden");
    const response = await fetch(`/upload?model=${encodeURIComponent(model)}`, {
      method: "POST",
      body: formData,
    });

    if (errorOccurred) return; // If an error came in during the wait, don't continue.
    // genWorkButton.classList.remove('hidden');
    clearButton.classList.remove("hidden");
    const data = await response.json();

    if (data.worklet_count) {
      totalWorklets = data.worklet_count;
    }
    console.log("printign data files");
    console.log(data.files);
    if (data.files) {
      receivedFiles = data.files;
    }

    loading.style.display = "none";
    progressContainer.style.display = "none";
    progressMessage.style.display = "none";

    // Place the two download buttons side by side in a flex container
    const downloadBtnContainer = document.createElement("div");
    downloadBtnContainer.style.display = "flex";
    downloadBtnContainer.style.gap = "16px";
    downloadBtnContainer.style.justifyContent = "center";
    downloadBtnContainer.style.marginTop = "20px";

    const downloadAllPdf = document.createElement("button");
    downloadAllPdf.classList.add("generate-btn");
    downloadAllPdf.textContent = "Download zip as PDF";
    downloadAllPdf.style.fontWeight = "700";
    downloadAllPdf.style.width = "auto";
    downloadAllPdf.style.minWidth = "160px";
    downloadAllPdf.style.marginTop = "0";

    const downloadAllPpt = document.createElement("button");
    downloadAllPpt.classList.add("generate-btn");
    downloadAllPpt.textContent = "Download zip as PPT";
    downloadAllPpt.style.fontWeight = "700";
    downloadAllPpt.style.width = "auto";
    downloadAllPpt.style.minWidth = "160px";
    downloadAllPpt.style.marginTop = "0";

    downloadBtnContainer.appendChild(downloadAllPdf);
    downloadBtnContainer.appendChild(downloadAllPpt);
    downloadList.appendChild(downloadBtnContainer);

    downloadAllPdf.addEventListener("click", async () => {
      if (receivedFiles.length === 0) {
        alert("No files to download.");
        return;
      }
      try {
        const response = await fetch("/download_all?type=pdf", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ files: receivedFiles }),
        });

        if (!response.ok) {
          throw new Error("Failed to download ZIP");
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "worklets_pdf.zip";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error("Download error:", error);
        alert("Error downloading ZIP file.");
      }
    });

    downloadAllPpt.addEventListener("click", async () => {
      if (receivedFiles.length === 0) {
        alert("No files to download.");
        return;
      }
      try {
        const response = await fetch("/download_all?type=ppt", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ files: receivedFiles }),
        });

        if (!response.ok) {
          throw new Error("Failed to download ZIP");
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "worklets_ppt.zip";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error("Download error:", error);
        alert("Error downloading ZIP file.");
      }
    });
  } catch (error) {
    if (errorOccurred) return;
    console.error("Error:", error);
    loading.style.display = "none";
    progressContainer.style.display = "none";
    progressMessage.style.display = "none";
    alert("An error occurred while generating worklets.");
  }
});

// Show query approval modal
socket.on("query_approval", (data) => {
  console.log("request received", data);
  const modal = document.getElementById("query-modal");
  const list = document.getElementById("query-list");
  list.innerHTML = ""; // clear old entries

  const heading = document.getElementById("show_message");
  heading.textContent =
    data.show_message || "Please approve or edit the queries:";

  if (!Array.isArray(data.queries)) return;

  data.queries.forEach((q, i) => {
    list.appendChild(createQueryInput(q));
  });

  modal.classList.remove("hidden");
  document.body.classList.add("modal-active");
});

function createQueryInput(value = "") {
  const wrapper = document.createElement("div");
  wrapper.className = "query-item";

  const input = document.createElement("input");
  input.type = "text";
  input.value = value;

  const removeBtn = document.createElement("button");
  removeBtn.className = "remove-query-btn";
  removeBtn.textContent = "✖";
  removeBtn.onclick = () => wrapper.remove();

  wrapper.appendChild(input);
  wrapper.appendChild(removeBtn);

  return wrapper;
}

document.getElementById("add-query-btn").addEventListener("click", () => {
  const list = document.getElementById("query-list");
  list.appendChild(createQueryInput());
});

document.getElementById("query-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const modal = document.getElementById("query-modal");
  const inputs = document.querySelectorAll("#query-list input");
  const updatedQueries = Array.from(inputs)
    .map((i) => i.value.trim())
    .filter((val) => val);

  socket.emit("query_response", { queries: updatedQueries, sid: sid });
  modal.classList.add("hidden");
  document.body.classList.remove("modal-active");
});

const observer = new MutationObserver(() => {
  const modalActive = document.body.classList.contains("modal-active");
  document.querySelector(".container").style.filter = modalActive
    ? "blur(5px)"
    : "";
});
observer.observe(document.body, {
  attributes: true,
  attributeFilter: ["class"],
});

//another one

socket.on("topic_approval", (data) => {
  const modal = document.getElementById("topic-modal");
  document.body.classList.add("modal-active");
  modal.classList.remove("hidden");

  const keywordSections = document.getElementById("keywords-sections");
  const domainSections = document.getElementById("domains-sections");
  keywordSections.innerHTML = "";
  domainSections.innerHTML = "";
  clearList("user-keywords-list");
  clearList("user-domains-list");

  populateSection(
    keywordSections,
    data.keywords.worklet_keywords,
    "Keywords extracted from worklets:",
    "keyword"
  );
  populateSection(
    keywordSections,
    data.keywords.link_keywords,
    "Keywords extracted from links:",
    "keyword"
  );
  populateSection(
    keywordSections,
    data.keywords.custom_prompt_keywords,
    "Keywords extracted from Custom prompt:",
    "keyword"
  );

  populateSection(
    domainSections,
    data.domains.worklet_domains,
    "Domains extracted from worklets:",
    "domain"
  );
  populateSection(
    domainSections,
    data.domains.link_domains,
    "Domains extracted from links:",
    "domain"
  );
  populateSection(
    domainSections,
    data.domains.custom_prompt_domains,
    "Domains extracted from Custom prompt:",
    "domain"
  );
});

function populateSection(container, items, label, type) {
  if (!items || items.length === 0) return;
  const section = document.createElement("div");
  section.className = "section";

  const title = document.createElement("h4");
  title.textContent = label;
  section.appendChild(title);

  items.forEach((item) => {
    section.appendChild(createItemEntry(item, type, section));
  });

  container.appendChild(section);
}

function createItemEntry(value, type, section) {
  const div = document.createElement("div");
  div.className = "item-entry";

  const input = document.createElement("input");
  input.type = "text";
  input.value = value;

  input.oninput = () => autoResizeInput(input);
  autoResizeInput(input); // Initial size

  const btn = document.createElement("button");
  btn.className = "remove-btn";
  btn.textContent = "✖";
  btn.onclick = () => {
    div.remove();
    const remainingInputs = section.querySelectorAll("input");
    if (remainingInputs.length === 0) {
      section.remove();
    }
  };

  div.appendChild(input);
  div.appendChild(btn);
  return div;
}

function clearList(id) {
  const container = document.getElementById(id);
  container.innerHTML = "";
}

document.getElementById("add-keyword-btn").addEventListener("click", () => {
  const list = document.getElementById("user-keywords-list");
  list.appendChild(createItemEntry("", "added_keyword", list));
});

document.getElementById("add-domain-btn").addEventListener("click", () => {
  const list = document.getElementById("user-domains-list");
  list.appendChild(createItemEntry("", "added_domain", list));
});

document.getElementById("submit-topics").addEventListener("click", () => {
  const keywords = collectSections("keywords-sections");
  const domains = collectSections("domains-sections");

  const added_keywords = collectUserItems("user-keywords-list");
  const added_domains = collectUserItems("user-domains-list");

  const payload = {
    keywords: {
      worklet_keywords: keywords["Keywords extracted from worklets:"] || [],
      link_keywords: keywords["Keywords extracted from links:"] || [],
      custom_prompt_keywords:
        keywords["Keywords extracted from Custom prompt:"] || [],
      added_keywords,
    },
    domains: {
      worklet_domains: domains["Domains extracted from worklets:"] || [],
      link_domains: domains["Domains extracted from links:"] || [],
      custom_prompt_domains:
        domains["Domains extracted from Custom prompt:"] || [],
      added_domains,
    },
  };

  socket.emit("topic_response", payload);
  document.getElementById("topic-modal").classList.add("hidden");
  document.body.classList.remove("modal-active");
});

function collectSections(containerId) {
  const data = {};
  const container = document.getElementById(containerId);
  const sections = container.querySelectorAll(".section");

  sections.forEach((sec) => {
    const label = sec.querySelector("h4")?.textContent;
    const inputs = sec.querySelectorAll("input");
    data[label] = Array.from(inputs)
      .map((i) => i.value.trim())
      .filter(Boolean);
  });

  return data;
}

function collectUserItems(listId) {
  const container = document.getElementById(listId);
  return Array.from(container.querySelectorAll("input"))
    .map((i) => i.value.trim())
    .filter(Boolean);
}

function autoResizeInput(input) {
  measurer.textContent = input.value || input.placeholder || "";
  const computedStyle = window.getComputedStyle(input);
  measurer.style.font = computedStyle.font;
  measurer.style.fontSize = computedStyle.fontSize;
  measurer.style.fontFamily = computedStyle.fontFamily;
  measurer.style.fontWeight = computedStyle.fontWeight;
  measurer.style.letterSpacing = computedStyle.letterSpacing;
  input.style.width = measurer.offsetWidth + 16 + "px"; 
}

const measurer = document.createElement("span");
measurer.className = "text-measurer";
document.body.appendChild(measurer);
