import test from "node:test";
import assert from "node:assert/strict";

import { isShortcutTargetBlocked, resolveChoiceNavigationIndex, resolveKeyboardAction } from "../web/app.js";

test("resolveKeyboardAction maps the bounded shortcut set", () => {
  assert.equal(resolveKeyboardAction({ key: "ArrowLeft", target: null }), "previous-slide");
  assert.equal(resolveKeyboardAction({ key: "ArrowRight", target: null }), "next-slide");
  assert.equal(resolveKeyboardAction({ key: " ", target: null }), "advance-reveal");
  assert.equal(resolveKeyboardAction({ key: "f", target: null }), "show-feedback");
  assert.equal(resolveKeyboardAction({ key: "R", target: null }), "reset-slide");
});

test("resolveKeyboardAction ignores blocked or modified events", () => {
  assert.equal(resolveKeyboardAction({ key: "ArrowLeft", ctrlKey: true, target: null }), null);
  assert.equal(resolveKeyboardAction({ key: "ArrowLeft", repeat: true, target: null }), null);
  assert.equal(resolveKeyboardAction({ key: "ArrowLeft", defaultPrevented: true, target: null }), null);
  assert.equal(resolveKeyboardAction({ key: "ArrowLeft", target: { tagName: "select" } }), null);
  assert.equal(resolveKeyboardAction({ key: "f", target: { tagName: "button" } }), null);
  assert.equal(resolveKeyboardAction({ key: " ", target: { isContentEditable: true } }), null);
});

test("isShortcutTargetBlocked recognizes interactive targets", () => {
  assert.equal(isShortcutTargetBlocked(null), false);
  assert.equal(isShortcutTargetBlocked({ tagName: "div" }), false);
  assert.equal(isShortcutTargetBlocked({ tagName: "input" }), true);
  assert.equal(isShortcutTargetBlocked({ tagName: "TEXTAREA" }), true);
  assert.equal(isShortcutTargetBlocked({ tagName: "button" }), true);
  assert.equal(isShortcutTargetBlocked({ isContentEditable: true }), true);
});

test("resolveChoiceNavigationIndex supports bounded arrow and edge-key movement", () => {
  assert.equal(resolveChoiceNavigationIndex(0, "ArrowRight", 3), 1);
  assert.equal(resolveChoiceNavigationIndex(1, "ArrowDown", 3), 2);
  assert.equal(resolveChoiceNavigationIndex(0, "ArrowLeft", 3), 2);
  assert.equal(resolveChoiceNavigationIndex(2, "ArrowUp", 3), 1);
  assert.equal(resolveChoiceNavigationIndex(2, "ArrowRight", 3), 0);
  assert.equal(resolveChoiceNavigationIndex(2, "Home", 3), 0);
  assert.equal(resolveChoiceNavigationIndex(0, "End", 3), 2);
});

test("resolveChoiceNavigationIndex ignores unrelated keys or empty choice sets", () => {
  assert.equal(resolveChoiceNavigationIndex(0, "Enter", 3), null);
  assert.equal(resolveChoiceNavigationIndex(0, " ", 3), null);
  assert.equal(resolveChoiceNavigationIndex(0, "ArrowRight", 0), null);
});