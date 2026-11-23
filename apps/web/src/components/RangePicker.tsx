import styles from "./PriceChart.module.css";

interface Props {
  options: number[];
  value: number;
  onChange: (days: number) => void;
}

/** Buttons to pick how many days the chart shows. */
export function RangePicker({ options, value, onChange }: Props) {
  return (
    <div className={styles.ranges} role="group" aria-label="Time range">
      {options.map((days) => (
        <button
          key={days}
          type="button"
          className={styles.range}
          aria-pressed={days === value}
          onClick={() => onChange(days)}
        >
          {days} d
        </button>
      ))}
    </div>
  );
}
