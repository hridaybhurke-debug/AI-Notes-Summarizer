
const titleInput = document.getElementById("meetingTitle");
const notesInput = document.getElementById("meetingNotes");

const generateBtn = document.getElementById("generateBtn");
const clearBtn = document.getElementById("clearBtn");

const statusText = document.getElementById("status");
const results = document.getElementById("results");

function getSentences(text) {
    return text
        .split(/[.!?\n]+/)
        .map(sentence => sentence.trim())
        .filter(sentence => sentence.length > 0);
}

function makeSummary(sentences) {
    // Temporary demo: use the first three sentences.
    return sentences.slice(0, 3).join(". ") + ".";
}

function findSentences(sentences, keywords) {
    return sentences.filter(sentence =>
        keywords.some(keyword =>
            sentence.toLowerCase().includes(keyword)
        )
    );
}

function displayList(elementId, items, emptyMessage) {
    const list = document.getElementById(elementId);
    list.replaceChildren();

    const displayItems = items.length ? items : [emptyMessage];

    displayItems.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        list.appendChild(li);
    });
}

generateBtn.addEventListener("click", () => {
    const notes = notesInput.value.trim();

    if (!notes) {
        statusText.textContent = "Please enter meeting notes first.";
        results.hidden = true;
        return;
    }

    const sentences = getSentences(notes);

    const summary = makeSummary(sentences);

    const decisions = findSentences(sentences, [
        "decided",
        "agreed",
        "approved",
        "confirmed",
        "decision"
    ]);

    const actions = findSentences(sentences, [
        "will ",
        "must ",
        "need to ",
        "assigned",
        "deadline"
    ]);

    document.getElementById("summary").textContent = summary;

    displayList(
        "decisions",
        decisions,
        "No decisions detected."
    );

    displayList(
        "actions",
        actions,
        "No action items detected."
    );

    results.hidden = false;

    statusText.textContent =
        "Summary generated for: " +
        (titleInput.value.trim() || "Untitled Meeting");
});

clearBtn.addEventListener("click", () => {
    titleInput.value = "";
    notesInput.value = "";
    results.hidden = true;
    statusText.textContent = "";
});