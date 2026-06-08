import type { ReactNode, InputHTMLAttributes, SelectHTMLAttributes } from "react";

export function Card({
  children,
  className = "",
  onClick,
}: {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
}) {
  return (
    <div
      onClick={onClick}
      className={`rounded-2xl bg-white shadow-sm border border-slate-100 p-4 ${
        onClick ? "active:scale-[0.99] cursor-pointer" : ""
      } ${className}`}
    >
      {children}
    </div>
  );
}

export function Button({
  children,
  onClick,
  variant = "primary",
  disabled,
  type = "button",
}: {
  children: ReactNode;
  onClick?: () => void;
  variant?: "primary" | "ghost" | "danger";
  disabled?: boolean;
  type?: "button" | "submit";
}) {
  const styles = {
    primary: "bg-brand-green text-white hover:bg-brand-greenDark",
    ghost: "bg-brand-greenLight text-brand-greenDark",
    danger: "bg-red-600 text-white hover:bg-red-700",
  }[variant];
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`w-full rounded-xl px-4 py-3 font-semibold transition disabled:opacity-50 ${styles}`}
    >
      {children}
    </button>
  );
}

export function Input(props: InputHTMLAttributes<HTMLInputElement> & { label?: string }) {
  const { label, ...rest } = props;
  return (
    <label className="block">
      {label && <span className="text-sm font-medium text-slate-600">{label}</span>}
      <input
        {...rest}
        className="mt-1 w-full rounded-xl border border-slate-200 px-4 py-3 text-slate-800 outline-none focus:border-brand-green focus:ring-2 focus:ring-brand-greenLight"
      />
    </label>
  );
}

export function Select(
  props: SelectHTMLAttributes<HTMLSelectElement> & { label?: string; options: string[]; placeholder?: string }
) {
  const { label, options, placeholder, ...rest } = props;
  return (
    <label className="block">
      {label && <span className="text-sm font-medium text-slate-600">{label}</span>}
      <select
        {...rest}
        className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-slate-800 outline-none focus:border-brand-green focus:ring-2 focus:ring-brand-greenLight disabled:opacity-50"
      >
        <option value="">{placeholder || "Select..."}</option>
        {options.map((o) => (
          <option key={o} value={o}>
            {o}
          </option>
        ))}
      </select>
    </label>
  );
}

export function Spinner({ label }: { label?: string }) {
  return (
    <div className="flex items-center justify-center gap-2 py-6 text-slate-400">
      <span className="h-4 w-4 animate-spin rounded-full border-2 border-slate-300 border-t-brand-green" />
      {label && <span className="text-sm">{label}</span>}
    </div>
  );
}

export function Banner({ tone = "info", children }: { tone?: "info" | "error" | "ok"; children: ReactNode }) {
  const styles = {
    info: "bg-blue-50 text-blue-700",
    error: "bg-red-50 text-red-700",
    ok: "bg-green-50 text-green-700",
  }[tone];
  return <div className={`rounded-xl px-4 py-3 text-sm ${styles}`}>{children}</div>;
}
