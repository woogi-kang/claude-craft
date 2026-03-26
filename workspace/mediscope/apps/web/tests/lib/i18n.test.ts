import { describe, it, expect } from "vitest";
import {
  SUPPORTED_LANGS,
  isValidLang,
  GUIDE_UI,
  LANG_LABELS,
  LANG_LOCALE,
} from "@/lib/i18n";

describe("i18n", () => {
  describe("SUPPORTED_LANGS", () => {
    it("should contain ko, en, ja, zh", () => {
      expect(SUPPORTED_LANGS).toEqual(["ko", "en", "ja", "zh"]);
    });
  });

  describe("isValidLang", () => {
    it("should return true for valid language codes", () => {
      for (const lang of SUPPORTED_LANGS) {
        expect(isValidLang(lang)).toBe(true);
      }
    });

    it("should return false for invalid language codes", () => {
      expect(isValidLang("fr")).toBe(false);
      expect(isValidLang("de")).toBe(false);
      expect(isValidLang("")).toBe(false);
      expect(isValidLang("KO")).toBe(false);
    });
  });

  describe("LANG_LABELS", () => {
    it("should have labels for all supported languages", () => {
      for (const lang of SUPPORTED_LANGS) {
        expect(LANG_LABELS[lang]).toBeDefined();
        expect(typeof LANG_LABELS[lang]).toBe("string");
      }
    });
  });

  describe("LANG_LOCALE", () => {
    it("should have locale codes for all supported languages", () => {
      for (const lang of SUPPORTED_LANGS) {
        expect(LANG_LOCALE[lang]).toBeDefined();
        expect(LANG_LOCALE[lang]).toMatch(/^[a-z]{2}_[A-Z]{2}$/);
      }
    });
  });

  describe("GUIDE_UI", () => {
    const requiredKeys = [
      "title",
      "subtitle",
      "procedureCount",
      "avgDiscount",
      "viewAll",
      "backToGuide",
      "priceCompare",
      "relatedProcedures",
      "recommendedClinics",
      "recoveryDays",
      "priceRange",
      "koreaPrice",
      "savings",
    ] as const;

    for (const lang of SUPPORTED_LANGS) {
      it(`should have all required keys for ${lang}`, () => {
        const ui = GUIDE_UI[lang];
        expect(ui).toBeDefined();
        for (const key of requiredKeys) {
          expect(ui[key]).toBeDefined();
          expect(typeof ui[key]).toBe("string");
          expect(ui[key].length).toBeGreaterThan(0);
        }
      });
    }
  });
});
