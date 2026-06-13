#!/usr/bin/env node

import { readFileSync } from "node:fs";
import { basename } from "node:path";

const [, , lottiePath, controlsPath] = process.argv;

if (!lottiePath) {
  console.error("Usage: validate-lottie.mjs <public/lottie.json> [public/controls.json]");
  process.exit(2);
}

const errors = [];
const warnings = [];

function readJson(path) {
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch (error) {
    errors.push(`${path}: invalid JSON (${error.message})`);
    return null;
  }
}

const doc = readJson(lottiePath);
const controls = controlsPath ? readJson(controlsPath) : null;

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function hasStaticArray(value, length) {
  return isObject(value) && value.a === 0 && Array.isArray(value.k) && value.k.length === length;
}

function pathLabel(parts) {
  return parts.join(".");
}

function walk(value, visit, path = []) {
  visit(value, path);
  if (Array.isArray(value)) {
    value.forEach((item, index) => walk(item, visit, [...path, String(index)]));
    return;
  }
  if (isObject(value)) {
    Object.entries(value).forEach(([key, child]) => walk(child, visit, [...path, key]));
  }
}

function collectGroupItems(shapeLayer) {
  const groups = [];
  for (const [shapeIndex, shape] of (shapeLayer.shapes ?? []).entries()) {
    if (!isObject(shape)) continue;
    if (shape.ty === "gr") {
      groups.push({ shape, path: `layers.${shapeLayer.__index}.shapes.${shapeIndex}` });
    }
  }
  return groups;
}

function findFillSids(layer) {
  const sids = [];
  walk(layer, (value, path) => {
    if (isObject(value) && typeof value.sid === "string" && path.at(-1) === "c") {
      sids.push(value.sid);
    }
  });
  return sids;
}

if (doc) {
  if (!isObject(doc)) {
    errors.push("Lottie document must be a JSON object.");
  } else {
    for (const key of ["v", "fr", "ip", "op", "w", "h", "assets", "layers"]) {
      if (!(key in doc)) errors.push(`Missing top-level field: ${key}`);
    }

    if (typeof doc.fr !== "number" || doc.fr <= 0) errors.push("fr must be a positive number.");
    if (typeof doc.w !== "number" || doc.w <= 0) errors.push("w must be a positive number.");
    if (typeof doc.h !== "number" || doc.h <= 0) errors.push("h must be a positive number.");
    if (typeof doc.ip !== "number" || typeof doc.op !== "number" || doc.op <= doc.ip) {
      errors.push("ip/op must be numbers and op must be greater than ip.");
    }
    if (!Array.isArray(doc.assets)) errors.push("assets must be an array, even when empty.");
    if (!Array.isArray(doc.layers)) errors.push("layers must be an array.");

    const layers = Array.isArray(doc.layers) ? doc.layers : [];
    layers.forEach((layer, index) => {
      if (!isObject(layer)) {
        errors.push(`layers.${index} must be an object.`);
        return;
      }
      layer.__index = index;
      if (typeof layer.ty !== "number") errors.push(`layers.${index}.ty must be present.`);
      if (typeof layer.ip !== "number" || typeof layer.op !== "number" || layer.op <= layer.ip) {
        errors.push(`layers.${index} must have numeric ip/op with op > ip.`);
      }
      if (!isObject(layer.ks)) errors.push(`layers.${index}.ks transform block is required.`);

      if (layer.ty === 4) {
        if (!Array.isArray(layer.shapes)) {
          errors.push(`layers.${index} is a shape layer but has no shapes array.`);
          return;
        }

        for (const [shapeIndex, shape] of layer.shapes.entries()) {
          if (!isObject(shape)) continue;
          if (["el", "rc", "sh", "fl", "st", "tr"].includes(shape.ty)) {
            errors.push(
              `layers.${index}.shapes.${shapeIndex} is a direct ${shape.ty} primitive; wrap primitives in a ty:"gr" group.`
            );
          }
        }

        const groups = collectGroupItems(layer);
        if (groups.length === 0 && layer.shapes.length > 0) {
          errors.push(`layers.${index} has shapes but no ty:"gr" group.`);
        }
        for (const { shape, path } of groups) {
          if (!Array.isArray(shape.it)) {
            errors.push(`${path}.it must be an array.`);
            continue;
          }
          const last = shape.it.at(-1);
          if (!isObject(last) || last.ty !== "tr") {
            errors.push(`${path}.it must end with a group transform ty:"tr".`);
          }
        }
      }
    });

    walk(doc, (value, path) => {
      if (!isObject(value)) return;

      if (value.a === 1 && Array.isArray(value.k) && value.k.every(isObject)) {
        for (const [index, keyframe] of value.k.entries()) {
          if ("s" in keyframe && !Array.isArray(keyframe.s)) {
            errors.push(`${pathLabel(path)}.k.${index}.s must be an array, including scalar properties.`);
          }
          if (typeof keyframe.t === "number" && typeof doc.ip === "number" && typeof doc.op === "number") {
            if (keyframe.t < doc.ip || keyframe.t > doc.op) {
              warnings.push(`${pathLabel(path)}.k.${index}.t (${keyframe.t}) is outside document ip/op.`);
            }
          }
        }
      }

      if (path.at(-1) === "c" && isObject(value) && Array.isArray(value.k)) {
        const color = value.k;
        if (color.length === 4 && color.some((component) => typeof component !== "number" || component < 0 || component > 1)) {
          errors.push(`${pathLabel(path)}.k must be normalized RGBA values between 0 and 1.`);
        }
      }
    });

    const slots = isObject(doc.slots) ? doc.slots : {};
    const slotIds = new Set(Object.keys(slots));
    const bgSlotIds = Object.entries(slots)
      .filter(([sid, slot]) => {
        const looksLikeBackground = /(^bg|background|backdrop)/i.test(sid);
        const value = slot?.p?.k;
        return looksLikeBackground && Array.isArray(value) && value.length === 4;
      })
      .map(([sid]) => sid);

    if (bgSlotIds.length === 0) {
      errors.push("A background color slot is required. Use a slot id like bgColor or backgroundColor.");
    }

    if (layers.length > 0 && bgSlotIds.length > 0) {
      const lastLayer = layers.at(-1);
      const lastLayerName = String(lastLayer?.nm ?? "");
      const fillSids = isObject(lastLayer) ? findFillSids(lastLayer) : [];
      const hasBgFill = fillSids.some((sid) => bgSlotIds.includes(sid));
      if (!/background|backdrop|bg/i.test(lastLayerName) && !hasBgFill) {
        errors.push("The last layer should be the background layer and use the background color slot.");
      }
      if (!hasBgFill) {
        errors.push(`The background layer must fill with one of these background slots: ${bgSlotIds.join(", ")}.`);
      }
      if (isObject(lastLayer) && lastLayer.ty === 4) {
        let hasFullRect = false;
        walk(lastLayer, (value) => {
          if (!isObject(value) || value.ty !== "rc") return;
          if (hasStaticArray(value.s, 2) && value.s.k[0] >= doc.w && value.s.k[1] >= doc.h) {
            hasFullRect = true;
          }
        });
        if (!hasFullRect) {
          warnings.push("Could not find a full-composition rectangle in the background layer.");
        }
      }
    }

    if (controls) {
      if (!isObject(controls) || !Array.isArray(controls.controls)) {
        errors.push(`${controlsPath}: expected an object with a controls array.`);
      } else {
        const controlSids = new Set();
        for (const [index, control] of controls.controls.entries()) {
          if (!isObject(control) || typeof control.sid !== "string") {
            errors.push(`controls.${index}.sid must be a string.`);
            continue;
          }
          controlSids.add(control.sid);
          if (!slotIds.has(control.sid)) {
            warnings.push(`controls.${index}.sid (${control.sid}) does not match any slot id.`);
          }
        }
        for (const bgSid of bgSlotIds) {
          if (!controlSids.has(bgSid)) {
            errors.push(`controls.json must include a label entry for background slot ${bgSid}.`);
          }
        }
      }
    } else if (bgSlotIds.length > 0) {
      errors.push("public/controls.json is required so the background color slot has a readable label.");
    }

    walk(doc, (value) => {
      if (isObject(value)) delete value.__index;
    });
  }
}

for (const warning of warnings) {
  console.warn(`WARN: ${warning}`);
}

if (errors.length > 0) {
  for (const error of errors) {
    console.error(`ERROR: ${error}`);
  }
  console.error(`\n${basename(lottiePath)} failed validation with ${errors.length} error(s).`);
  process.exit(1);
}

console.log(`${basename(lottiePath)} passed Lottie harness validation.`);
