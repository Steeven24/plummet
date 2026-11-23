import { type ThemeChoice, useTheme } from "../hooks/useTheme";

const OPTIONS: { value: ThemeChoice; label: string }[] = [
  { value: "light", label: "Light" },
  { value: "dark", label: "Dark" },
  { value: "system", label: "System" },
];

export function ThemeToggle() {
  const { choice, setChoice } = useTheme();
  return (
    <label>
      <span className="sr-only">Theme</span>
      <select
        className="input"
        value={choice}
        onChange={(event) => setChoice(event.target.value as ThemeChoice)}
      >
        {OPTIONS.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label} theme
          </option>
        ))}
      </select>
    </label>
  );
}
