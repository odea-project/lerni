const hasDom = typeof window !== "undefined" && typeof document !== "undefined";

const pageState = {
  manifest: null,
  deck: null,
  slideIndex: 0,
  runtimes: [],
  alertMessage: "",
};

const elements = hasDom ? {
  deckId: document.querySelector("#deck-id"),
  slideCount: document.querySelector("#slide-count"),
  deckPicker: document.querySelector("#deck-picker"),
  slidePicker: document.querySelector("#slide-picker"),
  deckMeta: document.querySelector("#deck-meta"),
  browserAlert: document.querySelector("#browser-alert"),
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
} : null;

if (hasDom) {
  void bootstrap();
}

async function bootstrap() {
  const manifestResponse = await fetch("./data/deck-manifest.json");
  if (!manifestResponse.ok) {
    throw new Error(`Failed to load deck manifest: ${manifestResponse.status}`);
  }

  pageState.manifest = await manifestResponse.json();
  wireEvents();
  populateDeckPicker();
  const initialState = resolveInitialUrlState(new URL(window.location.href), pageState.manifest);
  pageState.alertMessage = initialState.message;
  await loadDeck(initialState.deckId, initialState.slideIndex);
}

function wireEvents() {
  elements.previousSlide.addEventListener("click", () => {
    goToPreviousSlide();
  });

  elements.nextSlide.addEventListener("click", () => {
    goToNextSlide();
  });

  elements.advanceReveal.addEventListener("click", () => {
    advanceCurrentReveal();
  });

  elements.showFeedback.addEventListener("click", () => {
    showCurrentFeedback();
  });

  elements.resetSlide.addEventListener("click", () => {
    resetCurrentSlide();
  });

  elements.deckPicker.addEventListener("change", async (event) => {
    pageState.alertMessage = "";
    await loadDeck(event.target.value, 0);
  });

  elements.slidePicker.addEventListener("change", (event) => {
    pageState.alertMessage = "";
    pageState.slideIndex = normalizeSlideIndex(Number.parseInt(event.target.value, 10), pageState.deck.slides.length);
    render();
  });

  document.addEventListener("keydown", (event) => {
    const action = resolveKeyboardAction(event);
    if (!action) {
      return;
    }

    event.preventDefault();
    handleKeyboardAction(action);
  });
}

function goToPreviousSlide() {
  if (pageState.slideIndex === 0) {
    return false;
  }

  pageState.alertMessage = "";
  pageState.slideIndex -= 1;
  render();
  return true;
}

function goToNextSlide() {
  if (pageState.slideIndex >= pageState.deck.slides.length - 1) {
    return false;
  }

  pageState.alertMessage = "";
  pageState.slideIndex += 1;
  render();
  return true;
}

function advanceCurrentReveal() {
  const slide = getCurrentSlide();
  const runtime = getCurrentRuntime();
  if (runtime.currentRevealStep >= slide.runtime.maxRevealStep) {
    return false;
  }

  pageState.alertMessage = "";
  runtime.currentRevealStep += 1;
  render();
  return true;
}

function showCurrentFeedback() {
  const slide = getCurrentSlide();
  const runtime = getCurrentRuntime();
  if (!slide.interactions.includes("question_flow") || runtime.selectedAnswerIndex === null || runtime.feedbackVisible) {
    return false;
  }

  pageState.alertMessage = "";
  runtime.feedbackVisible = true;
  const feedbackStep = firstFeedbackStep(slide);
  if (feedbackStep !== null) {
    runtime.currentRevealStep = Math.max(runtime.currentRevealStep, feedbackStep);
  }
  render();
  return true;
}

function resetCurrentSlide() {
  pageState.alertMessage = "";
  pageState.runtimes[pageState.slideIndex] = createRuntimeState(getCurrentSlide());
  render();
  return true;
}

function selectAnswerChoice(answerIndex) {
  const runtime = getCurrentRuntime();
  if (runtime.selectedAnswerIndex !== null) {
    return false;
  }

  pageState.alertMessage = "";
  runtime.selectedAnswerIndex = answerIndex;
  render();

  if (hasDom && !elements.showFeedback.disabled) {
    elements.showFeedback.focus();
  }
  return true;
}

function handleKeyboardAction(action) {
  if (!pageState.deck) {
    return false;
  }

  if (action === "previous-slide") {
    return goToPreviousSlide();
  }
  if (action === "next-slide") {
    return goToNextSlide();
  }
  if (action === "advance-reveal") {
    return advanceCurrentReveal();
  }
  if (action === "show-feedback") {
    return showCurrentFeedback();
  }
  if (action === "reset-slide") {
    return resetCurrentSlide();
  }
  return false;
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

async function loadDeck(deckId, requestedSlideIndex = 0) {
  const manifestEntry = pageState.manifest.decks.find((entry) => entry.deckId === deckId);
  if (!manifestEntry) {
    throw new Error(`Unknown deck id: ${deckId}`);
  }

  const response = await fetch(manifestEntry.payloadPath);
  if (!response.ok) {
    throw new Error(`Failed to load deck payload '${deckId}': ${response.status}`);
  }

  pageState.deck = await response.json();
  pageState.slideIndex = normalizeSlideIndex(requestedSlideIndex, pageState.deck.slides.length);
  pageState.runtimes = pageState.deck.slides.map((slide) => createRuntimeState(slide));
  elements.deckPicker.value = deckId;
  populateSlidePicker();
  elements.deckMeta.textContent = `${manifestEntry.title} · ${manifestEntry.slideCount} slides · source ${manifestEntry.sourcePath}`;
  updateBrowserUrl(deckId, pageState.slideIndex);
  render();
}

function populateSlidePicker() {
  elements.slidePicker.innerHTML = "";
  pageState.deck.slides.forEach((slide, index) => {
    const option = document.createElement("option");
    option.value = String(index);
    option.textContent = buildSlideLabel(slide, index);
    elements.slidePicker.appendChild(option);
  });
}

function render() {
  const slide = getCurrentSlide();
  const runtime = getCurrentRuntime();
  const snapshot = computeSnapshot(slide, runtime);

  elements.deckId.textContent = pageState.deck.deckId;
  elements.slideCount.textContent = `${pageState.slideIndex + 1} / ${pageState.deck.slides.length}`;
  elements.slidePicker.value = String(pageState.slideIndex);
  elements.slideTemplate.textContent = slide.templateId;
  elements.slideKind.textContent = slide.slideKind ?? "untyped";

  renderAlert();
  renderSlide(slide, runtime, snapshot);
  renderRuntime(snapshot);
  renderControls(slide, snapshot);
  updateBrowserUrl(pageState.deck.deckId, pageState.slideIndex);
}

function renderAlert() {
  if (!pageState.alertMessage) {
    elements.browserAlert.classList.add("hidden");
    elements.browserAlert.textContent = "";
    return;
  }

  elements.browserAlert.classList.remove("hidden");
  elements.browserAlert.textContent = pageState.alertMessage;
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
  section.setAttribute("role", "group");

  const heading = document.createElement("h2");
  heading.className = "slot-title";
  heading.textContent = "answer choices";
  heading.id = "answer-choices-heading";
  section.appendChild(heading);

  const hint = document.createElement("p");
  hint.className = "choice-hint";
  hint.textContent = "Use Tab to enter choices, arrow keys to move, Enter or Space to choose.";
  section.appendChild(hint);

  const grid = document.createElement("div");
  grid.className = "quiz-choice-grid";
  grid.setAttribute("role", "radiogroup");
  grid.setAttribute("aria-labelledby", heading.id);

  const items = slot.blocks.flatMap((block) => block.items ?? []);
  items.forEach((item, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `quiz-choice${runtime.selectedAnswerIndex === index ? " selected" : ""}`;
    button.textContent = item;
    button.disabled = runtime.selectedAnswerIndex !== null;
    button.dataset.choiceIndex = String(index);
    button.setAttribute("role", "radio");
    button.setAttribute("aria-checked", String(runtime.selectedAnswerIndex === index));
    button.tabIndex = runtime.selectedAnswerIndex === null && index === 0 ? 0 : -1;
    button.addEventListener("click", () => {
      selectAnswerChoice(index);
    });
    button.addEventListener("keydown", (event) => {
      const nextIndex = resolveChoiceNavigationIndex(index, event.key, items.length);
      if (nextIndex === null) {
        return;
      }

      event.preventDefault();
      moveChoiceFocus(grid, index, nextIndex);
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

function resolveInitialUrlState(url, manifest) {
  const requestedDeckId = url.searchParams.get("deck");
  const requestedSlide = url.searchParams.get("slide");
  const availableDeckIds = manifest.decks.map((entry) => entry.deckId);
  const fallbackMessages = [];

  let deckId = manifest.defaultDeckId;
  if (requestedDeckId) {
    if (availableDeckIds.includes(requestedDeckId)) {
      deckId = requestedDeckId;
    } else {
      fallbackMessages.push(`Unknown deck '${requestedDeckId}'. Showing '${manifest.defaultDeckId}' instead.`);
    }
  }

  const selectedDeck = manifest.decks.find((entry) => entry.deckId === deckId);
  const slideCount = selectedDeck ? selectedDeck.slideCount : 1;

  let slideIndex = 0;
  if (requestedSlide !== null) {
    const parsedSlide = Number.parseInt(requestedSlide, 10);
    if (Number.isNaN(parsedSlide) || parsedSlide < 1) {
      fallbackMessages.push(`Invalid slide '${requestedSlide}'. Showing slide 1 instead.`);
    } else if (parsedSlide > slideCount) {
      slideIndex = Math.max(0, slideCount - 1);
      fallbackMessages.push(`Slide '${requestedSlide}' is out of range. Showing slide ${slideCount} instead.`);
    } else {
      slideIndex = parsedSlide - 1;
    }
  }

  return {
    deckId,
    slideIndex,
    message: fallbackMessages.join(" "),
  };
}

function updateBrowserUrl(deckId, slideIndex) {
  const url = new URL(window.location.href);
  url.searchParams.set("deck", deckId);
  url.searchParams.set("slide", String(slideIndex + 1));
  window.history.replaceState({}, "", url);
}

function normalizeSlideIndex(slideIndex, slideCount) {
  if (slideCount <= 0) {
    return 0;
  }
  if (slideIndex < 0) {
    return 0;
  }
  return Math.min(slideIndex, slideCount - 1);
}

function buildSlideLabel(slide, index) {
  const titleSlot = slide.slots.find((slot) => slot.slotName === "title");
  const titleBlock = titleSlot && titleSlot.blocks.length > 0 ? titleSlot.blocks[0] : null;
  const title = titleBlock && titleBlock.text ? titleBlock.text : `${slide.templateId}`;
  return `${index + 1}. ${title}`;
}

function moveChoiceFocus(grid, currentIndex, nextIndex) {
  const currentButton = grid.querySelector(`[data-choice-index="${currentIndex}"]`);
  const nextButton = grid.querySelector(`[data-choice-index="${nextIndex}"]`);
  if (!currentButton || !nextButton) {
    return false;
  }

  currentButton.tabIndex = -1;
  nextButton.tabIndex = 0;
  nextButton.focus();
  return true;
}

function resolveChoiceNavigationIndex(currentIndex, key, choiceCount) {
  if (choiceCount <= 0) {
    return null;
  }

  if (key === "Home") {
    return 0;
  }
  if (key === "End") {
    return choiceCount - 1;
  }
  if (key === "ArrowLeft" || key === "ArrowUp") {
    return currentIndex === 0 ? choiceCount - 1 : currentIndex - 1;
  }
  if (key === "ArrowRight" || key === "ArrowDown") {
    return currentIndex === choiceCount - 1 ? 0 : currentIndex + 1;
  }
  return null;
}

function isShortcutTargetBlocked(target) {
  if (!target) {
    return false;
  }

  const tagName = typeof target.tagName === "string" ? target.tagName.toUpperCase() : "";
  if (target.isContentEditable) {
    return true;
  }

  return ["INPUT", "TEXTAREA", "SELECT", "BUTTON"].includes(tagName);
}

function resolveKeyboardAction(event) {
  if (!event || event.defaultPrevented || event.repeat || event.altKey || event.ctrlKey || event.metaKey) {
    return null;
  }

  if (isShortcutTargetBlocked(event.target)) {
    return null;
  }

  if (event.key === "ArrowLeft") {
    return "previous-slide";
  }
  if (event.key === "ArrowRight") {
    return "next-slide";
  }
  if (event.key === " " || event.key === "Spacebar") {
    return "advance-reveal";
  }

  const normalizedKey = typeof event.key === "string" ? event.key.toLowerCase() : "";
  if (normalizedKey === "f") {
    return "show-feedback";
  }
  if (normalizedKey === "r") {
    return "reset-slide";
  }
  return null;
}

export {
  resolveChoiceNavigationIndex,
  isShortcutTargetBlocked,
  resolveKeyboardAction,
};