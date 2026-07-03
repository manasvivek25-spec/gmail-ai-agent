import React from "react"
import { cn } from "@/lib/utils"

const Badge = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { variant?: "default" | "secondary" | "destructive" | "outline" | "success" | "ai" }
>(({ className, variant = "default", ...props }, ref) => {
  const variants = {
    default: "border-transparent bg-primary text-white hover:bg-primary/80",
    secondary: "border-transparent bg-slate-100 text-slate-900 hover:bg-slate-100/80",
    destructive: "border-transparent bg-red-100 text-red-700",
    outline: "text-slate-950 border border-slate-200",
    success: "border-transparent bg-secondary/10 text-secondary",
    ai: "border-transparent bg-primary/10 text-primary",
  }

  return (
    <div
      ref={ref}
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-slate-950 focus:ring-offset-2",
        variants[variant],
        className
      )}
      {...props}
    />
  )
})
Badge.displayName = "Badge"

export { Badge }
