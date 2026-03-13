const pageState = {
  manifest: null,
  deck: null,
  slideIndex: 0,
  runtimes: [],
};

const elements = {
  deckId: document.querySelector("#deck-id"),
  slideCount: document.querySelector("#slide-count"),
  deckPicker: document.querySelector("#deck-picker"),
  deckMeta: document.querySelector("#deck-meta"),
  slideTemplate: document.querySelector("#slide-template"),
  slideKind: document.querySelector("#slide-kind"),
  slideContent: document.querySelector("#slide-content"),
  runtimeState: document.querySelector("#runtime-state"),
  snapshotPreview: document.querySelector("#snapshot-preview"),
  previousSlide: document.querySelector("#previous-slide"),
  nextSlide: document.querySelector("#next-slide"),
  advanceReveal: document.querySelector("#advance-reveal"),
  showFeedback: document.querySelector("#show-feedback"),
  resetSlide: document.querySelector("#reset-slide"),
};

void bootstrap();

async function bootstrap() {
  const manifestResponse = await fetch("./data/deck-manifest.json");
  if (!manifestResponse.ok) {
    throw new Error(`Failed to load deck manifest: ${manifestResponse.status}`);
  }

  pageState.manifest = await manifestResponse.json();
  wireEvents();
  populateDeckPicker();
  const requestedDeckId = new URL(window.location.href).searchParams.get("deck");
  const targetDeckId = resolveRequestedDeckId(requestedDeckId);
  await loadDeck(targetDeckId);
}

function wireEvents() {
  elements.previousSlide.addEventListener("click", () => {
    pageState.slideIndex = Math.max(0, pageState.slideIndex - 1);
    render();
  });

  elements.nextSlide.addEventListener("click", () => {
    pageState.slideIndex = Math.min(pageState.deck.slides.length - 1, pageState.slideIndex + 1);
    render();
  });

  elements.advanceReveal.addEventListener("click", () => {
    const slide = getCurrentSlide();
    const runtime = getCurrentRuntime();
    if (runtime.currentRevealStep < slide.runtime.maxRevealStep) {
      runtime.currentRevealStep += 1;
      render();
    }
  });

  elements.showFeedback.addEventListener("click", () => {
    const slide = getCurrentSlide();
    const runtime = getCurrentRuntime();
    if (!slide.interactions.includes("question_flow") || runtime.selectedAnswerIndex === null || runtime.feedbackVisible) {
      return;
    }

    runtime.feedbackVisible = true;
    const feedbackStep = firstFeedbackStep(slide);
    if (feedbackStep !== null) {
      runtime.currentRevealStep = Math.max(runtime.currentRevealStep, feedbackStep);
    }
    render();
  });

  elements.resetSlide.addEventListener("click", () => {
    pageState.runtimes[pageState.slideIndex] = createRuntimeState(getCurrentSlide());
    render();
  });

  elements.deckPicker.addEventListener("change", async (event) => {
    await loadDeck(event.target.value);
  });
}

function populateDeckPicker() {
  elements.deckPicker.innerHTML = "";
  pageState.manifest.decks.forEach((deck) => {
    const option = document.createElement("option");
    option.value = deck.deckId;
    option.textContent = `${deck.title} (${deck.slideCount})`;
    elements.deckPicker.appendChild(option);
  });
}

async function loadDeck(deckId) {
  const manifestEntry = pageState.manifest.decks.find((entry) => entry.deckId === deckId);
  if (!manifestEntry) {
    throw new Error(`Unknown deck id: ${deckId}`);
  }

  const response = await fetch(manifestEntry.payloadPath);
  if (!response.ok) {
    throw new Error(`Failed to load deck payload '${deckId}': ${response.status}`);
  }

  pageState.deck = await response.json();
  pageState.slideIndex = 0;
  pageState.runtimes = pageState.deck.slides.map((slide) => createRuntimeState(slide));
  elements.deckPicker.value = deckId;
  elements.deckMeta.textContent = `${manifestEntry.title} · ${manifestEntry.slideCount} slides · source ${manifestEntry.sourcePath}`;
  updateDeckUrl(deckId);
  render();
}

function render() {
  const slide = getCurrentSlide();
  const runtime = getCurrentRuntime();
  const snapshot = computeSnapshot(slide, runtime);

  elements.deckId.textContent = pageState.deck.deckId;
  elements.slideCount.textContent = `${pageState.slideIndex + 1} / ${pageState.deck.slides.length}`;
  elements.slideTemplate.textContent = slide.templateId;
  elements.slideKind.textContent = slide.slideKind ?? "untyped";

  renderSlide(slide, runtime, snapshot);
  renderRuntime(snapshot);
  renderControls(slide, snapshot);
}

function renderSlide(slide, runtime, snapshot) {
  elements.slideContent.className = `slide-content template-${slide.templateId}`;
  elements.slideContent.innerHTML = "";

  if (slide.templateId === "quiz-feedback") {
    renderQuizSlide(slide, runtime, snapshot);
    return;
  }

  slide.slotSequence.forEach((slotName) => {
    const slot = slide.slots.find((entry) => entry.slotName === slotName);
    elements.slideContent.appendChild(renderSlot(slot, runtime, snapshot, slide));
  });
}

function renderQuizSlide(slide, runtime, snapshot) {
  slide.slotSequence.forEach((slotName) => {
    const slot = slide.slots.find((entry) => entry.slotName === slotName);
    if (slotName === "answer_choices") {
      elements.slideContent.appendChild(renderAnswerChoices(slot, runtime));
      return;
    }
    elements.slideContent.appendChild(renderSlot(slot, runtime, snapshot, slide));
  });
}

function renderSlot(slot, runtime, snapshot, slide) {
  const section = document.createElement("section");
  section.className = "slot-card";
  section.dataset.slot = slot.slotName;

  const heading = document.createElement("h2");
  heading.className = "slot-title";
  heading.textContent = slot.slotName.replaceAll("_", " ");
  section.appendChild(heading);

  const slotSnapshot = snapshot.slotVisibility[slot.slotName];
  const visibleBlocks = slot.blocks.filter((block) => slotSnapshot.visibleBlockIds.includes(block.block_id));

  if (visibleBlocks.length === 0 && slot.slotName === "feedback") {
    const note = document.createElement("p");
    note.className = "hidden-slot-note";
    note.textContent = runtime.selectedAnswerIndex === null
      ? "Choose an answer, then reveal feedback."
      : "Feedback is ready to be revealed.";
    section.appendChild(note);
    return section;
  }

  visibleBlocks.forEach((block) => {
    section.appendChild(renderBlock(block, slot, slide));
  });
  return section;
}

function renderBlock(block, slot, slide) {
  const wrapper = document.createElement("div");
  wrapper.className = "content-block";

  if (block.kind === "heading") {
    const heading = document.createElement("h3");
    heading.className = slot.slotName === "title" && slide.templateId === "title-overview" ? "overview-title" : "slot-heading";
    heading.textContent = block.text ?? "";
    wrapper.appendChild(heading);
    return wrapper;
  }

  if (block.kind === "paragraph") {
    const paragraph = document.createElement("p");
    paragraph.textContent = block.text ?? "";
    wrapper.appendChild(paragraph);
    return wrapper;
  }

  if (block.kind === "list") {
    const list = document.createElement("ul");
    block.items.forEach((item) => {
      const entry = document.createElement("li");
      entry.textContent = item;
      list.appendChild(entry);
    });
    wrapper.appendChild(list);
    return wrapper;
  }

  if (block.kind === "code") {
    const pre = document.createElement("pre");
    pre.textContent = block.code ?? "";
    wrapper.appendChild(pre);
    return wrapper;
  }

  return wrapper;
}

function renderAnswerChoices(slot, runtime) {
  const section = document.createElement("section");
  section.className = "slot-card";
  section.dataset.slot = slot.slotName;

  const heading = document.createElement("h2");
  heading.className = "slot-title";
  heading.textContent = "answer choices";
  section.appendChild(heading);

  const grid = document.createElement("div");
  grid.className = "quiz-choice-grid";

  const items = slot.blocks.flatMap((block) => block.items ?? []);
  items.forEach((item, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `quiz-choice${runtime.selectedAnswerIndex === index ? " selected" : ""}`;
    button.textContent = item;
    button.disabled = runtime.selectedAnswerIndex !== null;
    button.addEventListener("click", () => {
      runtime.selectedAnswerIndex = index;
      render();
    });
    grid.appendChild(button);
  });
  section.appendChild(grid);

  return section;
}

function renderRuntime(snapshot) {
  const entries = [
    ["mode", snapshot.activeMode],
    ["reveal step", `${snapshot.currentRevealStep} / ${snapshot.maxRevealStep}`],
    ["can advance", String(snapshot.canAdvanceReveal)],
    ["selected answer", snapshot.selectedAnswerIndex === null ? "none" : String(snapshot.selectedAnswerIndex)],
    ["feedback visible", String(snapshot.feedbackVisible)],
  ];

  elements.runtimeState.innerHTML = "";
  entries.forEach(([label, value]) => {
    const term = document.createElement("dt");
    term.textContent = label;
    const definition = document.createElement("dd");
    definition.textContent = value;
    elements.runtimeState.appendChild(term);
    elements.runtimeState.appendChild(definition);
  });

  elements.snapshotPreview.textContent = JSON.stringify(snapshot, null, 2);
}

function renderControls(slide, snapshot) {
  elements.previousSlide.disabled = pageState.slideIndex === 0;
  elements.nextSlide.disabled = pageState.slideIndex === pageState.deck.slides.length - 1;
  elements.advanceReveal.disabled = !snapshot.canAdvanceReveal;
  elements.showFeedback.disabled = !slide.interactions.includes("question_flow") || snapshot.selectedAnswerIndex === null || snapshot.feedbackVisible;
}

function createRuntimeState(slide) {
  const initial = slide.runtime.initialSnapshot;
  return {
    currentRevealStep: initial.currentRevealStep,
    selectedAnswerIndex: initial.selectedAnswerIndex,
    feedbackVisible: initial.feedbackVisible,
  };
}

function computeSnapshot(slide, runtime) {
  const slotVisibility = {};
  slide.slots.forEach((slot) => {
    const visibleBlockIds = [];
    const hiddenBlockIds = [];
    slot.blocks.forEach((block) => {
      const revealReady = block.reveal_step === null || block.reveal_step <= runtime.currentRevealStep;
      const isVisible = slot.slotName === "feedback" ? runtime.feedbackVisible && revealReady : revealReady;
      if (isVisible) {
        visibleBlockIds.push(block.block_id);
      } else {
        hiddenBlockIds.push(block.block_id);
      }
    });
    slotVisibility[slot.slotName] = {
      slotName: slot.slotName,
      visibleBlockIds,
      hiddenBlockIds,
    };
  });

  return {
    slideId: slide.slideId,
    templateId: slide.templateId,
    currentRevealStep: runtime.currentRevealStep,
    maxRevealStep: slide.runtime.maxRevealStep,
    canAdvanceReveal: runtime.currentRevealStep < slide.runtime.maxRevealStep,
    selectedAnswerIndex: runtime.selectedAnswerIndex,
    feedbackVisible: runtime.feedbackVisible,
    activeMode: deriveActiveMode(slide, runtime),
    slotVisibility,
  };
}

function deriveActiveMode(slide, runtime) {
  if (runtime.feedbackVisible) {
    return "feedback";
  }
  if (slide.interactions.includes("question_flow")) {
    return "question";
  }
  if (slide.runtime.maxRevealStep > 0) {
    return "reveal";
  }
  return "content";
}

function firstFeedbackStep(slide) {
  const feedbackSlot = slide.slots.find((slot) => slot.slotName === "feedback");
  if (!feedbackSlot) {
    return null;
  }
  const steps = feedbackSlot.blocks
    .map((block) => block.reveal_step)
    .filter((step) => step !== null)
    .sort((left, right) => left - right);
  return steps.length > 0 ? steps[0] : null;
}

function getCurrentSlide() {
  return pageState.deck.slides[pageState.slideIndex];
}

function getCurrentRuntime() {
  return pageState.runtimes[pageState.slideIndex];
}

function resolveRequestedDeckId(requestedDeckId) {
  if (requestedDeckId && pageState.manifest.decks.some((entry) => entry.deckId === requestedDeckId)) {
    return requestedDeckId;
  }
  return pageState.manifest.defaultDeckId;
}

function updateDeckUrl(deckId) {
  const url = new URL(window.location.href);
  url.searchParams.set("deck", deckId);
  window.history.replaceState({}, "", url);
}