import js from "@eslint/js";
import globals from "globals";
import pluginReact from "eslint-plugin-react";
import vitest from "eslint-plugin-vitest";
import { defineConfig } from "eslint/config";

export default defineConfig([
  {
    ignores: ["dist/**", "node_modules/**"],  // ✅ stop linting compiled code
  },
  {
    files: ["**/*.{js,mjs,cjs,jsx}"],
    plugins: {
      js,
      react: pluginReact,
      vitest,
    },
    extends: [
      js.configs.recommended,
      pluginReact.configs.flat.recommended,
      vitest.configs.recommended,
    ],
    languageOptions: {
      globals: {
        ...globals.browser,
        ...vitest.environments.env.globals,
      },
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
      },
    },
    settings: {
      react: { version: "detect" },
    },
    rules: {
      "react/react-in-jsx-scope": "off",
    },
  },
]);
