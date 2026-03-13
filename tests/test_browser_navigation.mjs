import test from "node:test";
import assert from "node:assert/strict";

import { isShortcutTargetBlocked, resolveKeyboardAction } from "../web/app.js";

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